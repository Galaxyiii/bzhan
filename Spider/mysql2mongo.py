# MongoDB
M_HOST = "localhost"  # 数据库host
M_PORT = 27017  # 数据库端口

from database.mysql_db import query_by_sql
import pymongo

def get_mysql_data():
    sql = """SELECT * FROM `bilibili` WHERE `play` IS NOT NULL"""
    return query_by_sql(sql)

def insert_data_into_mongo(client, data):
    mydb = client["bzhan"]
    mycol = mydb["bilibili"]
    # 修改数据集，为每个文档添加`_id`字段
    for item in data:
        item["_id"] = item["id"]
    try:
        x = mycol.insert_many(data)
        # 可选：输出插入的ID
        # print(x.inserted_ids)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # 连接到MongoDB
    myclient = pymongo.MongoClient(M_HOST, M_PORT)
    data = get_mysql_data()
    insert_data_into_mongo(myclient, data)
