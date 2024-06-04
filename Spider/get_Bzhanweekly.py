import pymongo
import requests
import time
import json
import pandas as pd
from retry import retry

# MongoDB 设置
M_HOST = "localhost"
M_PORT = 27017
M_USER = None
M_PASSWORD = None

client = pymongo.MongoClient(host=M_HOST, port=M_PORT, username=M_USER, password=M_PASSWORD)
mydb = client["bzhan"]

@retry()
def getWeek_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
        "referer": "https://www.bilibili.com/",
        "origin": "https://www.bilibili.com/"
    }
    response = requests.get(url=url, headers=headers, timeout=10)
    response_data = response.json()
    time.sleep(1)
    return response_data


def clean_data(video):
    # 定义需要检查的统计值键
    necessary_stats = ['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'like']

    # 检查统计值是否符合条件
    if any(int(video['stat'].get(stat, 1)) <= 0 for stat in necessary_stats) or int(
            video['stat'].get('dislike', 0)) > 0:
        return None  # 如果不符合条件，返回None表示数据不被接受

    # 检查描述和推荐理由是否为空，若为空则用标题填充
    if not video['desc'] or video['desc'] == '-':
        video['desc'] = video['title']
    if 'rcmd_reason' in video and (not video['rcmd_reason'] or video['rcmd_reason'] == '-'):
        video['rcmd_reason'] = video['title']

    # 清洗文本数据，删除逗号、分号、换行符等
    text_fields = ['title', 'desc', 'rcmd_reason']
    for field in text_fields:
        if field in video:
            video[field] = video[field].replace(',', ' ').replace(';', ' ').replace('\n', ' ').replace('\r',' ').replace('\t', ' ')
    return video

def insert_data_to_mongodb(json_data):
    key = ['up', 'time', 'title', 'desc', 'view', 'danmaku', 'reply', 'favorite',
           'coin', 'share', 'like', 'rcmd_reason', 'tname', 'his_rank']
    rows = []
    for video in json_data['data']['list']:
        # 检查并清理数据
        if not clean_data(video):
            continue
        row_data = {
            'up': video['owner']['name'],
            'time': json_data['data']['config']['name'],
            'title': video['title'],
            'desc': video['desc'],
            'view': video['stat']['view'],
            'danmaku': video['stat']['danmaku'],
            'reply': video['stat']['reply'],
            'favorite': video['stat']['favorite'],
            'coin': video['stat']['coin'],
            'share': video['stat']['share'],
            'like': video['stat']['like'],
            'rcmd_reason': video.get('rcmd_reason', ''),
            'tname': video['tname'],
            'his_rank': video['stat']['his_rank']
        }
        rows.append(row_data)
    if rows:
        mydb['bilibili_weekly'].insert_many(rows)

if __name__ == '__main__':
    url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'
    for i in range(147, 264):
        url_formatted = url.format(str(i))
        json_data = getWeek_json(url_formatted)
        if json_data:
            insert_data_to_mongodb(json_data)

    print("数据处理完毕")