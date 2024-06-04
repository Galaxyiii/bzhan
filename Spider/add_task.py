import requests
import json
from database.mysql_db import do_by_sql
import datetime


params = {
    # "main_ver": "v3",           # 版本信息，已注释
    "search_type": "video",      # 搜索类型，这里是视频
    "view_type": "hot_rank",     # 查看类型，热度排行
    "order": "click",            # 排序方式，按点击量排序
    "copy_right": -1,            # 版权类型，-1表示所有
    "cate_id": "231",            # 分类ID
    "page": 2,                   # 页码
    "pagesize": 100,             # 每页视频数
    "jsonp": "jsonp",            # 数据格式，使用JSONP
    "time_from": "20231201",     # 开始时间
    "time_to": "20231210",       # 结束时间
    # "callback": ""             # 回调函数，已注释
}

cates = [
    201, # 科学科普
    124, # 社科 法律 心理
    228, # 人文历史
    207, # 财经商业
    208, # 校园学习
    209, # 职业职场
    229, # 设计·创意
    122, # 野生技能协会
    95, # 数码
    230, # 软件应用
    231, # 计算机技术
    232, # 科工机械
    233 # 极客DIY
]

page_size = 100

tm = [
    ("20231201", "20231210"),  # 2023年12月1-10日
]


data = [[i, cate, time_from, time_to] for time_from, time_to in tm for cate in cates for i in range(1, page_size+1)]
sql = """INSERT INTO `task` (`page`, `cate_id`, `time_from`, `time_to`) VALUES (%s, %s, %s, %s)"""
do_by_sql(sql, data)
# do_by_sql(sql, data)

print(data[2:4])