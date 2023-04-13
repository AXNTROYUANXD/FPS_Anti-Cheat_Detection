import csv

# 读取csv文件并按ID进行分组
with open('fin.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows_by_id = {}
    for row in reader:
        rows_by_id.setdefault(row['ID'], []).append(row)

# 根据firstShootRate从每个ID组中选择最大的行
max_rows = []
for id_rows in rows_by_id.values():
    max_row = max(id_rows, key=lambda r: float(r['firstShootRate']))
    max_rows.append(max_row)

# 将结果写入新的csv文件
with open('new_fin.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(max_rows)
