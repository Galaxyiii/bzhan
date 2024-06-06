from pyspark import SparkContext
from pyspark.sql import SparkSession, Row

import json # 用于后面的流程

import os
import re
import jieba
from pyspark.sql.types import StringType, IntegerType, StructField, StructType

stopwords = [i.strip() for i in open('chineseStopWords.txt',encoding='utf-8').readlines()]

def pretty_cut(sentence):
    cut_list = jieba.lcut(''.join(re.findall('[\u4e00-\u9fa5]', sentence)), cut_all=False)
    for i in range(len(cut_list) - 1, -1, -1):
        if cut_list[i] in stopwords:
            del cut_list[i]
    return cut_list

def initialize(txt_file):
    # 创建SparkContext和SparkSession对象
    sc = SparkContext('local', 'spark_project')
    sc.setLogLevel('WARN')
    spark = SparkSession.builder.getOrCreate()
    # 把数据加载为RDD，并且对每一行数据进行切割，转为Row对象
    rdd = spark.sparkContext.textFile(txt_file)\
        .map(lambda x: x.split("\t")).map(lambda x:Row(x[0],x[1],x[2],x[3],int(x[4]),int(x[5]),int(x[6]),\
                                                        int(x[7]),int(x[8]),int(x[9]),int(x[10]),x[11],x[12],int(x[13])))
    # 定义数据集结构
    fields = [StructField("up", StringType(), False), StructField("time", StringType(), False),
              StructField("title", StringType(), False),StructField("desc", StringType(), False),
              StructField("view", IntegerType(), False), StructField("danmaku", IntegerType(), False),
              StructField("reply", IntegerType(), False), StructField("favorite", IntegerType(), False),
              StructField("coin", IntegerType(), False), StructField("share", IntegerType(), False),
              StructField("like", IntegerType(), False), StructField("rcmd_reason", StringType(), False),
              StructField("tname", StringType(), False), StructField("his_rank", IntegerType(), False), ]
    schema = StructType(fields)
    # 将RDD转为Dataframe
    data = spark.createDataFrame(rdd, schema)
    # 注册sql临时视图
    data.createOrReplaceTempView("data")
    return spark

# 入选次数最多的10个up主
def top_popular_up(spark,base_dir):
    popular_up = spark.sql(
        "SELECT up,COUNT(up) AS popular_up_times FROM data GROUP BY up ORDER BY popular_up_times DESC LIMIT 10")
    data = popular_up.toPandas()
    save_dir = os.path.join(base_dir,'top_popular_up.csv')
    data.to_csv(save_dir,index=False)

# 入选次数最多的10个主题
def top_popular_subject(spark,base_dir):
    popular_subject = spark.sql(
        "SELECT tname,COUNT(tname) AS popular_subject_times FROM data GROUP BY tname ORDER BY popular_subject_times DESC LIMIT 10")
    data = popular_subject.toPandas()
    save_dir = os.path.join(base_dir,'top_popular_subject.csv')
    data.to_csv(save_dir, index=False)

# 播放量最多的10个视频与总播放量最多的10个up主
def top_popular_view(spark,base_dir):
    view_data = spark.sql(
        "SELECT title,view AS view_data FROM data ORDER BY view DESC LIMIT 10")
    data = view_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_view_data.csv')
    data.to_csv(save_dir,index=False)

    view_data = spark.sql(
        "SELECT up,sum(view) AS view_data FROM data GROUP BY up ORDER BY sum(view) DESC LIMIT 10")
    data = view_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_view_data.csv')
    data.to_csv(save_dir,index=False)

# 弹幕数量最多的10个视频与总弹幕数量最多的10个up主
def top_popular_danmaku(spark,base_dir):
    danmaku_data = spark.sql(
        "SELECT title,danmaku AS danmaku_data FROM data ORDER BY danmaku DESC LIMIT 10")
    data = danmaku_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_danmaku_data.csv')
    data.to_csv(save_dir, index=False)

    danmaku_data = spark.sql(
        "SELECT up,sum(danmaku) AS danmaku_data FROM data GROUP BY up ORDER BY sum(danmaku) DESC LIMIT 10")
    data = danmaku_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_danmaku_data.csv')
    data.to_csv(save_dir, index=False)

# 回复量最多的10个视频与总回复量最多的10个up主
def top_popular_reply(spark,base_dir):
    reply_data = spark.sql(
        "SELECT title,reply AS reply_data FROM data ORDER BY reply DESC LIMIT 10")
    data = reply_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_reply_data.csv')
    data.to_csv(save_dir, index=False)

    reply_data = spark.sql(
        "SELECT up,sum(reply) AS reply_data FROM data GROUP BY up ORDER BY sum(reply) DESC LIMIT 10")
    data = reply_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_reply_data.csv')
    data.to_csv(save_dir, index=False)

# 收藏次数最多的10个视频与总收藏次数最多的10个up主
def top_popular_favorite(spark,base_dir):
    favorite_data = spark.sql(
        "SELECT title,favorite AS favorite_data FROM data ORDER BY favorite DESC LIMIT 10")
    data = favorite_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_favorite_data.csv')
    data.to_csv(save_dir, index=False)

    favorite_data = spark.sql(
        "SELECT up,sum(favorite) AS favorite_data FROM data GROUP BY up ORDER BY sum(favorite) DESC LIMIT 10")
    data = favorite_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_favorite_data.csv')
    data.to_csv(save_dir, index=False)

# 投币数最多的10个视频与总投币数最多的10个up主
def top_popular_coin(spark,base_dir):
    coin_data = spark.sql(
        "SELECT title,coin AS coin_data FROM data ORDER BY coin DESC LIMIT 10")
    data = coin_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_coin_data.csv')
    data.to_csv(save_dir, index=False)

    coin_data = spark.sql(
        "SELECT up,sum(coin) AS coin_data FROM data GROUP BY up ORDER BY sum(coin) DESC LIMIT 10")
    data = coin_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_coin_data.csv')
    data.to_csv(save_dir, index=False)

# 分享次数最多的10个视频与总分享次数最多的10个up主
def top_popular_share(spark,base_dir):
    share_data = spark.sql(
        "SELECT title,share AS share_data FROM data ORDER BY share DESC LIMIT 10")
    data = share_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_share_data.csv')
    data.to_csv(save_dir, index=False)

    share_data = spark.sql(
        "SELECT up,sum(share) AS share_data FROM data GROUP BY up ORDER BY sum(share) DESC LIMIT 10")
    data = share_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_share_data.csv')
    data.to_csv(save_dir, index=False)

# 点赞数最多的10个视频与总点赞数最多的10个up主
def top_popular_like(spark,base_dir):
    like_data = spark.sql(
        "SELECT title,like AS like_data FROM data ORDER BY like DESC LIMIT 10")
    data = like_data.toPandas()
    save_dir = os.path.join(base_dir,'video_like_data.csv')
    data.to_csv(save_dir, index=False)

    like_data = spark.sql(
        "SELECT up,sum(like) AS like_data FROM data GROUP BY up ORDER BY sum(like) DESC LIMIT 10")
    data = like_data.toPandas()
    save_dir = os.path.join(base_dir,'up_like_data.csv')
    data.to_csv(save_dir, index=False)

# 词频统计
def word_count(spark, base_dir):
    # 统计标题所有词的词频
    wordCount_title = spark.sql("SELECT title as title from data").rdd.flatMap(
        lambda line: pretty_cut(line['title'])).map(lambda word: (word, 1)).reduceByKey(
        lambda a, b: a + b).repartition(1).sortBy(lambda x: x[1], False)
    # 转为Dataframe
    wordCountSchema = StructType([StructField("word", StringType(), True), StructField("count", IntegerType(), True)])
    wordCountDF = spark.createDataFrame(wordCount_title, wordCountSchema)
    # 过滤掉空值
    wordCountDF = wordCountDF.filter(wordCountDF["word"] != '')
    # 只保留频数前300的单词
    wordCount_title_300 = wordCountDF.take(300)
    wordCount_title_300 = spark.createDataFrame(wordCount_title_300, wordCountSchema).toPandas()
    # 保存为csv文件
    save_dir = os.path.join(base_dir, 'title_word.csv')
    wordCount_title_300.to_csv(save_dir, index=False)

    # 视频简介词频统计，操作同上
    wordCount_desc = spark.sql("SELECT desc as description from data").rdd.flatMap(
        lambda line: pretty_cut(line['description'])).map(lambda word: (word, 1)).reduceByKey(
        lambda a, b: a + b).repartition(1).sortBy(lambda x: x[1], False)
    wordCountSchema = StructType([StructField("word", StringType(), True), StructField("count", IntegerType(), True)])
    wordCountDF = spark.createDataFrame(wordCount_desc, wordCountSchema)
    wordCountDF = wordCountDF.filter(wordCountDF["word"] != '')
    wordCount_desc_300 = wordCountDF.take(300)
    wordCount_desc_300 = spark.createDataFrame(wordCount_desc_300, wordCountSchema).toPandas()
    save_dir = os.path.join(base_dir, 'desc_word.csv')
    wordCount_desc_300.to_csv(save_dir, index=False)

    # 视频简介词频统计，操作同上
    wordCount_rcmd_reason = spark.sql("SELECT rcmd_reason as rcmd_reason from data").rdd.flatMap(
        lambda line: pretty_cut(line['rcmd_reason'])).map(lambda word: (word, 1)).reduceByKey(
        lambda a, b: a + b).repartition(1).sortBy(lambda x: x[1], False)
    wordCountSchema = StructType([StructField("word", StringType(), True), StructField("count", IntegerType(), True)])
    wordCountDF = spark.createDataFrame(wordCount_rcmd_reason, wordCountSchema)
    wordCountDF = wordCountDF.filter(wordCountDF["word"] != '')
    wordCount_rcmd_reason_300 = wordCountDF.take(300)
    wordCount_rcmd_reason_300 = spark.createDataFrame(wordCount_rcmd_reason_300, wordCountSchema).toPandas()
    save_dir = os.path.join(base_dir, 'rcmd_reason_word.csv')
    wordCount_rcmd_reason_300.to_csv(save_dir, index=False)



if __name__ == '__main__':
    # HDFS文件路径
    txt_file = 'hdfs://hadoop102:8020/input/bilibili_week.txt'
    # 初始化
    spark = initialize(txt_file)
    # 分析结果的存储路径
    base_dir = 'static/'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir,exist_ok=True)
    # 开始进行分析
    # 分析视频入选最多的up主
    top_popular_up(spark, base_dir)
    # 分析视频入选最多的视频分区
    top_popular_subject(spark, base_dir)
    # 分析播放量
    top_popular_view(spark,base_dir)
    # 分析弹幕数
    top_popular_danmaku(spark, base_dir)
    # 分析评论数
    top_popular_reply(spark, base_dir)
    # 分析收藏数
    top_popular_favorite(spark, base_dir)
    # 分析投币数
    top_popular_coin(spark, base_dir)
    # 分析分享次数
    top_popular_share(spark, base_dir)
    # 分析点赞数量
    top_popular_like(spark, base_dir)
    # 分析词频
    word_count(spark, base_dir)