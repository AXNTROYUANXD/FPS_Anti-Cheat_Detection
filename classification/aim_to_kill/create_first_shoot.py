import csv
import os


# 定义删减规则函数
def remove_duplicate_rows(data):
    i = 0
    while i < len(data) - 2:
        if data[i]['playerName'] == data[i + 1]['playerName']:
            data.pop(i + 1)
            data.pop(i + 1)
        elif data[i]['playerName'] == data[i + 2]['playerName']:
            data.pop(i + 2)
        else:
            i += 1


# 定义处理函数
def process_file(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    remove_duplicate_rows(data)
    with open(file_path.replace('_weaponFires', '_firstshoot'), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)


# 遍历文件夹
folder_path = 'path'
for filename in os.listdir(folder_path):
    if filename.endswith('_weaponFires.csv'):
        file_path = os.path.join(folder_path, filename)
        process_file(file_path)
