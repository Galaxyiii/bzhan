import os
from jieba import cut
from gensim.similarities import SparseMatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.corpora import MmCorpus
import numpy as np
from fastapi import APIRouter, Form
from Backend.functions.many_video_info import get_videos_info_by_ids
from Backend.basic import *

router = APIRouter(
    prefix="/video-recommend",
    tags=["video-recommend"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

def get_absolute_path(relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(script_dir, relative_path)
    return abs_path

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

model_path = get_absolute_path("data\VideoTitle-TFIDF.model")
aid_path = get_absolute_path("data\VideoTitle-Aid.txt")
dictionary_path = get_absolute_path("data\VideoTitle-Dic.dic")
corpus_path = get_absolute_path("data\VideoTitle-Corpus.corpus")

# Check if files exist
check_file_exists(model_path)
check_file_exists(aid_path)
check_file_exists(dictionary_path)
check_file_exists(corpus_path)

# Load model
print("正在加载模型...")
model = TfidfModel.load(model_path)

# Load aid
print("正在加载Aid...")
aids = [aid.strip() for aid in open(aid_path, "r").readlines()]

# Load dictionary
print("正在加载字典...")
dictionary = Dictionary.load(dictionary_path)

# Load corpus
print("正在加载语料库...")
corpus = MmCorpus(corpus_path)

# Get sparse matrix
print("正在计算稀疏矩阵...")
num_features = len(dictionary.token2id)
texts = model[corpus]
sparse_matrix = SparseMatrixSimilarity(texts, num_features)

@router.post('/recommend-video-by-text')
async def recommend_video_by_text(text: str = Form("")):
    '''
    通过文本匹配视频标题获得数据
    :param text 文本
    '''
    vector = dictionary.doc2bow(cut(text))
    tf = model[vector]
    similarities = sparse_matrix.get_similarities(tf)
    res = get_videos_info_by_ids([aids[x] for x in np.argsort(similarities)[-20:]])
    views = [x["stat"]["view"] for x in res]
    temp = np.argsort(views)
    index = np.argsort([0.99 * t + 0.01 * temp[t] for t in range(len(temp))])
    return successResponse(detail="返回成功", data=[res[i] for i in reversed(index)])

@router.post('/recommend-video-by-videos')
async def recommend_video_by_text(videos: str = Form("")):
    '''
    通过视频匹配视频标题获得数据
    :param videos 视频编号字符串以","为分隔符
    '''
    videos_list = videos.split(",")
    res = get_videos_info_by_ids(videos_list)
    text = [x['title'] for x in res]
    text = ' '.join(text)
    vector = dictionary.doc2bow(cut(text))
    tf = model[vector]
    similarities = sparse_matrix.get_similarities(tf)
    res = get_videos_info_by_ids([aids[x] for x in np.argsort(similarities)[-20:]])
    views = [x["stat"]["view"] for x in res]
    temp = np.argsort(views)
    index = np.argsort([0.99 * t + 0.01 * temp[t] for t in range(len(temp))])
    return successResponse(detail="返回成功", data=[res[i] for i in reversed(index)])

if __name__ == "__main__":
    lst = [
        "236501624",
        "236503250",
        "236503810"
    ]
    videos  = ','.join(lst)
    video_list = videos.split(",")
    res = get_videos_info_by_ids(video_list)
    text = [x['title'] for x in res]
    print(text)
