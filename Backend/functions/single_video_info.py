from fastapi import FastAPI, APIRouter, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import aiohttp
import asyncio
import nest_asyncio

from Backend.basic import successResponse, failResponse
from Backend.database.db import query_overall_situation, query_words_count, query_overall_situation_day, \
    query_tags_count_by_word, query_tag_count_change, query_tags_count_in_day, query_tags_relation

nest_asyncio.apply()

app = FastAPI()

# 设置允许的源
origins = [
    "http://localhost:4000",
    "http://localhost:8000",
    # 添加其他需要允许的源
]

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的HTTP方法
    allow_headers=["*"],  # 允许的HTTP头
)

router = APIRouter(
    prefix="/all-video",
    tags=["all-video"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

PAGE_SIZE = 20  # 一次获取多少评论
done = []

async def aiohttpget(aid, page):
    async with aiohttp.ClientSession(headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52",
            "Cookie": "SESSDATA=c0b9cd69%2C1732282039%2Ca7d5a%2A52CjCJ__nqAafKIeILjjvaTA1b3yWDA7_lUR3XBlDTlDa9SHrdXu9suCd8m4-vBthBmrkSVlRoSkVLckw3NWk3eXhSOVhxenEtRklfQm55U2NsU3FVMHViQUZnOGJRRV95NWdyanVVM2phV2tXNTN5aDBDQVhkc0Z2VDJTalk4Y3pxNl9xZ25ZaXdnIIEC"
        }) as session:
        async with session.get(
            url="https://api.bilibili.com/x/v2/reply/main",
            params={
                "mode": 3,  # 仅按热度
                "oid": aid,  # av号
                "next": page,  # 第几页 每次20条
                "type": 1   # 默认
            }
        ) as resp:
            return await resp.text()

async def main_gather(data_size, aid):
    task_gets = [asyncio.create_task(
        aiohttpget(aid, page)) for page in range(1, 1+(data_size + PAGE_SIZE - 1)//PAGE_SIZE)]  # 向上取整
    global done
    done = await asyncio.gather(*task_gets)

def get_basic_info_by_id(aid=None, bid=None, full=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        resp = requests.get(
            url="http://api.bilibili.com/x/web-interface/view",
            params={
                "aid": aid,
                "bvid": bid
            },
            headers=headers
        )
        resp.raise_for_status()  # Check if request was successful
        print("===get_basic_info_by_id===")
        #print(resp.text)  # 打印响应文本
        data = resp.json().get("data", {})
        if not data:
            raise ValueError("No data found in the response")

        needed_data = ["aid", "title", "desc", "stat", "pic", "bvid", "owner"]
        return {x: data[x] for x in needed_data} if not full else data
    except Exception as e:
        raise Exception(f"获取视频基本信息错误: {str(e)}")

def get_replies_info_by_aid(aid, data_size=50):
    global done
    done = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_gather(data_size, aid))
    ans = []
    for data in done:
        try:
            replies_data = json.loads(data).get("data", {})
            replies = replies_data.get("replies", [])
            ans.extend([reply["content"]["message"] for reply in replies])
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            print(f"Error processing replies data: {e}")
            continue
    return ans

def get_video_info_by_id(aid=None, bid=None):
    if aid is None and bid is None:
        raise Exception("请给出aid或者bid的其中一种")
    aid = aid.lower().strip("av") if isinstance(aid, str) else aid
    info = get_basic_info_by_id(aid, bid)
    try:
        aid = info["aid"]
        info["replies"] = get_replies_info_by_aid(aid=aid)
        return info
    except Exception as e:
        raise Exception(f"获取评论错误: {str(e)}")

@router.post('/all-video-info')
async def all_video_info(num: int = Form(20)):
    data = {}
    data['play_data'] = query_overall_situation()
    data['words_count'] = query_words_count(num)  # 词云使用
    data['play_data_forlinechart'] = query_overall_situation_day()
    rate_data = {}
    for x in data['play_data']:
        if x['fq'] + '-' + x['cate'] not in rate_data.keys():
            rate_data[x['fq'] + '-' + x['cate']] = 0
        rate_data[x['fq'] + '-' + x['cate']] += x['num']
    line_data = {}
    for x in data['play_data_forlinechart']:
        if x['day'] not in line_data.keys():
            line_data[x['day']] = {}
        line_data[x['day']][x['fq'] + '-' + x['cate']] = x['num']
    data['rate_data'] = rate_data
    data['line_data'] = line_data
    return successResponse(detail="视频基本信息返回成功", data=data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-by-word')
async def tags_count_by_word(word: str = Form(""), num: int = Form(50)):
    data = {}
    data['tags_count_by_word'] = query_tags_count_by_word(word, num)
    return successResponse(detail="视频基本信息返回成功", data=data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-change')
async def tags_count_change(tag: str = Form("")):
    data = {}
    data['tags_count_change'] = query_tag_count_change(tag)
    return successResponse(detail="视频基本信息返回成功", data=data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-count-in-day')
async def tags_count_in_day(day: int = Form(None), num: int = Form(10)):
    data = {}
    data['tags_count_in_day'] = query_tags_count_in_day(day, num)
    return successResponse(detail="视频基本信息返回成功", data=data) if data != None else failResponse(detail="视频基本信息返回失败")

@router.post('/tags-relation')
async def tags_relation(tags: str = Form()):
    data = {}
    tags = tags.split(",")
    data['tags_relation'] = query_tags_relation(tags)
    return successResponse(detail="视频基本信息返回成功", data=data) if data != None else failResponse(detail="视频基本信息返回失败")

app.include_router(router)
