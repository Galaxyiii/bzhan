#
# import os
# import os.path
#
# def dfs_showdir(path, depth):
#     if depth == 0:
#         print("root:[" + path + "]")
#
#     for item in os.listdir(path):
#         if '.git' not in item:
#             print("| " * depth + "+--" + item)
#
#             newitem = path +'/'+ item
#             if os.path.isdir(newitem):
#                 dfs_showdir(newitem, depth +1)
#
# if __name__ == '__main__':
#     dfs_showdir('.', 0)

# import csv
# from datetime import datetime
#
# # 输入和输出文件路径
# input_file = 'bzhan.bilibili.csv'
# output_file = 'bilibili_tag_date.csv'
#
# # 读取 CSV 文件并进行修改
# with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8',
#                                                                   newline='') as outfile:
#     reader = csv.DictReader(infile)
#     fieldnames = ['id', 'tag', 'pubdate']
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for row in reader:
#         # 修改 tag 字段，替换分隔符
#         row['tag'] = row['tag'].replace(',', '|')
#
#         # 修改 pubdate 字段，只保留日期中的日
#         date_obj = datetime.fromisoformat(row['pubdate'].replace('Z', '+00:00'))
#         row['pubdate'] = str(date_obj.day)
#
#         writer.writerow(row)
#
# print("CSV 文件已成功修改。")

# import csv
#
# # 输入和输出文件路径
# input_file = 'bilibili_week_waitingforprocess.csv'
# output_file = 'bilibili_week_waitingfortrain.csv'
#
# # 读取 CSV 文件并进行修改
# with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8',
#                                                                   newline='') as outfile:
#     reader = csv.DictReader(infile)
#     # 移除不需要的字段
#     fieldnames = [field for field in reader.fieldnames if field not in ['time', 'title']]
#
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     for row in reader:
#         # 移除不需要的字段
#         row.pop('time', None)
#         row.pop('title', None)
#
#         writer.writerow(row)
#
# print("CSV 文件已成功修改。")

import csv

# 输入和输出文件路径
input_file = 'bilibili_week_waitingforprocess.csv'
output_file = 'bilibili_week_train.csv'

# 读取 CSV 文件并进行修改
with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8',
                                                                  newline='') as outfile:
    reader = csv.DictReader(infile)
    # 移除不需要的字段
    fieldnames = [field for field in reader.fieldnames if field not in ['time', 'title']]

    writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONE, escapechar='\\')
    writer.writeheader()

    for row in reader:
        # 移除不需要的字段
        row.pop('time', None)
        row.pop('title', None)

        writer.writerow(row)

print("CSV 文件已成功修改。")
