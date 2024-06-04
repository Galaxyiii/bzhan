from pyspark import SparkConf, SQLContext, SparkContext
from pyspark.sql import SparkSession
import jieba

M_HOST = "localhost"
M_PORT = 27017
M_USER = None
M_PASSWORD = None

# 构建 MongoDB URI
auth_params = ""
if M_USER and M_PASSWORD:
    auth_params = f"{M_USER}:{M_PASSWORD}@"

mongodb_read_uri = f"mongodb://{auth_params}{M_HOST}:{M_PORT}/bzhan.bilibili"
mongodb_write_uri = f"mongodb://{auth_params}{M_HOST}:{M_PORT}/bzhan.result"

spark = SparkSession \
    .builder \
    .appName("TitleWordsAnalysis") \
    .master("spark://master:7077") \
    .config("spark.mongodb.read.connection.uri", mongodb_read_uri) \
    .config("spark.mongodb.write.connection.uri", mongodb_write_uri) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.rpc.message.maxSize", 1024) \
    .getOrCreate()

def process_string(string):
    return string.replace(" ", "").replace("\n", "").replace("\t", "")

def get_stop_words(filepath):
    stopwords = spark.textFile(filepath).collect()
    stopwords = [x.strip() for x in stopwords]
    return stopwords

print("正在加载数据库...")
df = spark.read.format("mongodb").load()
print("数据库加载成功！\n正在执行Title数据预处理和分词...")
string = df.select("title").rdd.map(lambda x: x[0]).reduce(lambda x, y : x + y)
string = process_string(string)
words_list = jieba.lcut(string)

print("正在进行MapReduce统计结果...")
wordsRdd = spark.sparkContext.parallelize(words_list)
stop_words = get_stop_words("stop_words.txt")
resRdd = wordsRdd.filter(lambda word: word not in stop_words) \
                    .filter(lambda word: len(word) > 1) \
                    .map(lambda word: (word, 1)) \
                    .reduceByKey(lambda a, b: a + b) \
                    .sortBy(ascending=False, numPartitions=None, keyfunc=lambda x: x[1])
resDF = resRdd.toDF()
print("MapReduce结束！\n正在保存结果...")
resDF.write.format("mongodb").mode("append").save()
print("结果保存成功")
