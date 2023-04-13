import os
import pandas as pd

# 遍历timeToSwitch文件夹下的所有用户文件
folder_path = 'timeToSwitch'
for file_name in os.listdir(folder_path):
    if file_name.endswith('_timeToSwitch.csv'):
        file_path = os.path.join(folder_path, file_name)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 将相同player_name、round_num、weapon和weapon_after的行保留tick_change列数值最大的那一行，而删除其他相同行
        df = df.sort_values(['player_name', 'round_num', 'weapon', 'weapon_after', 'tick_change'], ascending=[True, True, True, True, False])
        df = df.drop_duplicates(subset=['player_name', 'round_num', 'weapon', 'weapon_after'], keep='first')

        # 保存处理后的CSV文件
        df.to_csv(file_path, index=False)
