# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Author  : SUN Chenxin
# @Time    : 24/2/2023 12:43 am
# @File    : time_to_kill_deduplication.py
import os
import pandas as pd

# 定义timeToKill文件夹路径
timeToKill_dir = 'timeToKill'

# 遍历timeToKill文件夹下的所有用户文件
for file in os.listdir(timeToKill_dir):
    if file.endswith('_timeToKill.csv'):
        print(file)
        # 读取csv文件并删除重复内容和kill_tick为负数的行
        df = pd.read_csv(os.path.join(timeToKill_dir, file))
        df.drop_duplicates(subset=['attackerName', 'victimSteamID', 'roundNum'], inplace=True)
        df = df[df['kill_tick'] >= 0]
        # 将处理后的数据保存到同名文件中
        df.to_csv(os.path.join(timeToKill_dir, file), index=False)
