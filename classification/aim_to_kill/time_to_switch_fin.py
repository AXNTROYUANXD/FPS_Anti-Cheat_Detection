import csv
import os

# 读取timeToSwitch文件夹下所有csv文件中的player_name和tick_change列
data = {}
for filename in os.listdir('timeToSwitch'):
    if filename.endswith('_timeToSwitch.csv'):
        with open(f'timeToSwitch/{filename}', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['player_name'] not in data or float(row['tick_change']) < float(data[row['player_name']]):
                    data[row['player_name']] = row['tick_change']

# 将合并处理后的数据保存至timeToSwitchfin.csv
with open('timeToSwitchfin.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'switchtick'])
    for key, value in data.items():
        writer.writerow([key, value])

# 将fin.csv和timeToSwitchfin.csv合并保存至fin1.csv
with open('fin.csv', 'w', newline='') as fin_file, open('timeToSwitchfin.csv', 'w', newline='') as switch_file, open(
        'fin1.csv', 'w', newline='') as fout_file:
    fin_reader = csv.DictReader(fin_file)
    switch_reader = csv.DictReader(switch_file)
    fieldnames = fin_reader.fieldnames + ['switchtick']
    fout_writer = csv.DictWriter(fout_file, fieldnames=fieldnames)
    fout_writer.writeheader()
    switch_dict = {row['ID']: row['switchtick'] for row in switch_reader}
    for row in fin_reader:
        row['switchtick'] = switch_dict.get(row['ID'], 0)
        fout_writer.writerow(row)
