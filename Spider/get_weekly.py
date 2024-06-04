import requests
import time
import os
import json
from retry import retry
from fake_useragent import UserAgent

@retry( )
def getWeek_json(url,json_path):
    # 随机User-Agent
    random_UA =  UserAgent().random
    # headers信息，添加user-agent和cookies
    headers = {
        "User-Agent": random_UA,
        "referer": "https://www.bilibili.com/",
        "origin": "https://www.bilibili.com/"
    }
    # 获取响应，转为json格式并保存
    response = requests.get(url=url,headers=headers,timeout=10)
    response_data = response.json()
    with open(json_path, 'w',encoding='utf-8') as f:
        json.dump(response_data, f,ensure_ascii=False)
    # 休眠，确保不会被反爬
    time.sleep(1)



if __name__=='__main__':
    # 官方api
    url='https://api.bilibili.com/x/web-interface/popular/series/one?number={}'
    # 爬虫数据存储路径
    data_folder = 'F:\下载的项目\myBzhan_data\data'
    os.makedirs(data_folder, exist_ok=True)
    # 开始爬虫
    for i in range(147,264): #统计2022-2024年4月15日前一周的每周必看
        URL = url.format(str(i))
        # 每周数据存储路径
        json_fpath = os.path.join(data_folder,'week_{}.json'.format(str(i)))
        getWeek_json(URL,json_fpath)