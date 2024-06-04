import os
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import when, col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier,DecisionTreeClassifier,LogisticRegression,GBTClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator,BinaryClassificationEvaluator
from pyspark.sql.types import StringType, IntegerType, StructField, StructType
from pyspark.ml.stat import Correlation
import pandas as pd

def initialize(txt_file):
    sc = SparkContext('local', 'spark_project')
    sc.setLogLevel('WARN')
    spark = SparkSession.builder.getOrCreate()
    fields = [StructField("up", StringType(), False), StructField("time", StringType(), False),
              StructField("title", StringType(), False),StructField("desc", StringType(), False),
              StructField("view", IntegerType(), False), StructField("danmaku", IntegerType(), False),
              StructField("reply", IntegerType(), False), StructField("favorite", IntegerType(), False),
              StructField("coin", IntegerType(), False), StructField("share", IntegerType(), False),
              StructField("like", IntegerType(), False), StructField("rcmd_reason", StringType(), False),
              StructField("tname", StringType(), False), StructField("his_rank", IntegerType(), False), ]
    schema = StructType(fields)
    rdd = spark.sparkContext.textFile(txt_file)\
        .map(lambda x: x.split("\t")).map(lambda x:Row(x[0],x[1],x[2],x[3],int(x[4]),int(x[5]),int(x[6]),\
                                                        int(x[7]),int(x[8]),int(x[9]),int(x[10]),x[11],x[12],int(x[13])))
    data = spark.createDataFrame(rdd, schema)
    return data

def transform_data(df):
    # 删除掉无用的数据
    df = df.drop('up')
    df = df.drop('time')
    df = df.drop('title')
    df = df.drop('desc')
    df = df.drop('rcmd_reason')
    df = df.drop('tname')
    # 根据历史排名his_rank，新增类别标签label
    df = df.withColumn('label', when(df.his_rank <= 10, 1).otherwise(0))

    # 将数据转为特征向量
    required_features = ['view','danmaku','reply','favorite','coin','share','like']
    assembler = VectorAssembler(
        inputCols=required_features,
        outputCol='features')
    transformed_data = assembler.transform(df)

    #对数据进行划分
    (training_data, test_data) = transformed_data.randomSplit([0.8, 0.2], seed=2023)
    print("训练数据集总数: " + str(training_data.count()))
    print("测试数据集总数: " + str(test_data.count()))
    return transformed_data,training_data,test_data

def corr_matrix(df,cor_save_dir):
    cor_mat = Correlation.corr(df, "features", "spearman").head()[0]
    cor_df = pd.DataFrame(cor_mat.toArray())
    cor_df.columns = ['view','danmaku','reply','favorite','coin','share','like']
    cor_df.to_csv(cor_save_dir, index=False)


def LogisticReg(training_data,test_data):
    # 实例化逻辑回归算法
    lr = LogisticRegression(labelCol='label',featuresCol='features',maxIter=15)
    # 进行模型训练
    model = lr.fit(training_data)
    # 进行模型验证
    lr_predictions = model.transform(test_data)
    # 计算分类acc
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol='label', metricName='accuracy')
    acc = multi_evaluator.evaluate(lr_predictions)
    print('LogisticRegression classifier Accuracy:{:.4f}'.format(acc))
    # 计算模型auc
    binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label",
        metricName="areaUnderROC")
    auc = binary_evaluator.evaluate(lr_predictions)
    print('LogisticRegression classifier Auc:{:.4f}'.format(auc))
    return ['LogisticRegression',acc,auc]

def DecisionTree(training_data,test_data):
    # 实例化决策树算法
    dt = DecisionTreeClassifier(labelCol='label',
                                featuresCol='features',
                                maxDepth =5)
    # 进行模型训练
    model = dt.fit(training_data)
    # 进行模型验证
    dt_predictions = model.transform(test_data)
    # 计算分类acc
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol='label', metricName='accuracy')
    acc = multi_evaluator.evaluate(dt_predictions)
    print('DecisionTree classifier Accuracy:{:.4f}'.format(acc))
    # 计算模型auc
    binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label",
        metricName="areaUnderROC")
    auc = binary_evaluator.evaluate(dt_predictions)
    print('DecisionTree classifier Auc:{:.4f}'.format(auc))
    return ['DecisionTree',acc,auc]

def Randomforest(training_data,test_data):
    # 实例化随机森林算法
    rf = RandomForestClassifier(labelCol='label',
                                featuresCol='features',
                                maxDepth=5)
    # 进行模型训练
    model = rf.fit(training_data)
    # 进行模型验证
    rf_predictions = model.transform(test_data)
    # 计算分类acc
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol='label', metricName='accuracy')
    acc = multi_evaluator.evaluate(rf_predictions)
    print('Random Forest classifier Accuracy:{:.4f}'.format(acc))
    # 计算模型auc
    binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label",
        metricName="areaUnderROC")
    auc = binary_evaluator.evaluate(rf_predictions)
    print('Random Forest classifier Auc:{:.4f}'.format(auc))
    return ['Random Forest',acc,auc]


def GBT(training_data,test_data):
    # 实例化GBT算法
    gb = GBTClassifier(labelCol='label',featuresCol='features',maxDepth=5)
    # 进行模型训练
    model = gb.fit(training_data)
    # 进行模型预测
    gb_predictions = model.transform(test_data)
    # 计算分类acc
    multi_evaluator = MulticlassClassificationEvaluator(labelCol='label', metricName='accuracy')
    acc = multi_evaluator.evaluate(gb_predictions)
    print('GBT classifier Accuracy:{:.4f}'.format(acc))
    # 计算模型auc
    binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label",
        metricName="areaUnderROC")
    auc = binary_evaluator.evaluate(gb_predictions)
    print('GBT classifier Auc:{:.4f}'.format(auc))
    return ['GBT',acc,auc]



def train(df,cor_dir,classifier_comparison_dir):
    transformed_data,training_data, test_data = transform_data(df)
    # 计算变量之间的相关性
    corr_matrix(transformed_data,cor_dir)
    # 使用四种分类器进行分类
    log_res = LogisticReg(training_data, test_data)
    dt_res = DecisionTree(training_data, test_data)
    rf_res = Randomforest(training_data, test_data)
    gbt_res = GBT(training_data, test_data)
    # 将分类器的性能结果保存在csv文件中
    classifier_comparison = [log_res,dt_res,rf_res,gbt_res]
    comparison_df = pd.DataFrame(classifier_comparison)
    comparison_df.columns = ['classifier','Acc','Auc']
    comparison_df.to_csv(classifier_comparison_dir,index = False)

if __name__ == '__main__':
    csv_file = 'hdfs://localhost:9000/user/hadoop/bilibili_week.txt'
    static_dir = './static'
    cor_save = os.path.join(static_dir,'cor_matrix.csv')
    classifier_comparison_dir = os.path.join(static_dir,'comparison.csv')
    df = initialize(csv_file)
    train(df,cor_save,classifier_comparison_dir)