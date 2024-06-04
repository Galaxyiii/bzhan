from fastapi import FastAPI, APIRouter, Form
from fastapi.middleware.cors import CORSMiddleware
from Backend.basic import *
from Backend.database.db import query_overall_situation, query_words_count, query_tags_count_by_word, \
    query_tag_count_change, query_tags_count_in_day, query_tags_relation, query_overall_situation_day

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

@router.post('/all-video-info')
async def all_video_info(num: int = Form(20)):
    data = {}
    data['play_data'] = query_overall_situation()
    data['words_count'] = query_words_count(num) # 词云使用
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
