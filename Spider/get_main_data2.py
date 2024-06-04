import time
import requests
import pymysql
from datetime import datetime
import pymysql.cursors

# 数据库连接设置
db = pymysql.connect(host="localhost", user="root", password="123456qwe", database="bzhan",cursorclass=pymysql.cursors.DictCursor)

def fetch_data_from_api(task):
    # 格式化日期
    date_from = datetime.strptime(task['time_from'], '%Y%m%d').strftime('%Y%m%d')
    date_to = datetime.strptime(task['time_to'], '%Y%m%d').strftime('%Y%m%d')

    # 构建搜索API请求
    search_url = f"https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id={task['cate_id']}&page={task['page']}&pagesize=100&jsonp=jsonp&time_from={date_from}&time_to={date_to}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
    }
    response_search = requests.get(search_url, headers=headers)
    videos = response_search.json().get('result', [])

    video_count = 0
    for video in videos:
        video_url = f"http://api.bilibili.com/x/web-interface/view?aid={video['id']}"
        # response_video = requests.get(video_url)
        response_video = requests.get(video_url, headers=headers)
        video_data = response_video.json().get('data', {})
        video_data['tag'] = video.get('tag', '')  # 将搜索结果中的标签添加到视频数据中
        # print(video_data)
        if insert_video_data(video_data):
            video_count += 1
        # time.sleep(2)  # Sleep after processing each video

    return video_count, len(videos)

def insert_video_data(video):
    try:
        required_keys = ['aid', 'title', 'pubdate', 'duration', 'owner', 'stat']
        if not all(key in video for key in required_keys):
            print(f"Video data is incomplete: {video['aid']}")
            return False

        # 如果某个嵌套键可能不存在，应该进行检查
        if 'mid' not in video['owner'] or 'view' not in video['stat']:
            print(f"Video data is incomplete in nested fields: {video}")
            return False

        with db.cursor() as cursor:
            # 先查询数据库是否已存在相同的数据
            sql_check = "SELECT * FROM bilibili WHERE id = %s"
            cursor.execute(sql_check, (video['aid'],))
            result = cursor.fetchone()
            if result:  # 如果已存在相同数据，则不进行插入
                print(f"Video data already exists in the database: {video['aid']}")
                return True

            sql = """INSERT INTO bilibili (id, title, tag, pubdate, description, duration, mid, play, video_review, review, favorites, coin, share, rank_index, `like`)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                video['aid'],
                video['title'],
                video['tag'],
                datetime.fromtimestamp(video['pubdate']),
                video.get('desc', '无描述'),
                video['duration'],
                video['owner']['mid'],
                video['stat']['view'],
                video['stat'].get('danmaku', 0),  # 使用get方法提供默认值
                video['stat'].get('reply', 0),
                video['stat'].get('favorite', 0),
                video['stat'].get('coin', 0),
                video['stat'].get('share', 0),
                video['stat'].get('his_rank', 0),
                video['stat'].get('like', 0)
            ))
            db.commit()
        return True
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return False
    except KeyError as e:
        print(f"Missing expected video field: {e}")
        return False

def update_task_status(task_id, status):
    try:
        with db.cursor() as cursor:
            sql = "UPDATE task SET finish = %s WHERE id = %s"
            cursor.execute(sql, (status, task_id))
            db.commit()
    except pymysql.Error as e:
        print(f"Database error: {e}")

def handle_tasks():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM task WHERE finish = -1")
        tasks = cursor.fetchall()

        for task in tasks:
            print(f"Processing task: {task['id']}")  # 开始处理任务
            update_task_status(task['id'], -1)  # 标记任务为正在处理

            videos_processed, total_videos = fetch_data_from_api(task)  # 处理API数据

            if videos_processed == total_videos:
                update_task_status(task['id'], -2)  # 所有视频处理完成，标记任务完成
                print(f"Task {task['id']} completed successfully with all {total_videos} videos processed.")
            else:
                missed_videos = total_videos - videos_processed  # 计算未成功处理的视频数量
                update_task_status(task['id'], missed_videos)  # 更新任务状态为未完全成功处理的视频数量
                print(f"Task {task['id']} completed with {missed_videos} missed videos out of {total_videos}.")

            print("一个任务完成...")
            print("===开始休眠===")
            time.sleep(5)  # 完成一个任务后休眠5秒，避免请求过于频繁

if __name__ == '__main__':
    handle_tasks()
