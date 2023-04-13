import os
import pandas as pd
import csv

# 定义文件路径和名称
dir_path = 'firstShootHitRate'
output_file = 'firstHitRate.csv'
input_file = 'fin.csv'
output_file1 = 'fin1.csv'

# 读取所有csv文件并合并为一个DataFrame
df_list = []
for file_name in os.listdir(dir_path):
    if file_name.endswith('_firstShootHitRate.csv'):
        file_path = os.path.join(dir_path, file_name)
        df = pd.read_csv(file_path, usecols=['name', 'rate'])
        df['name'] = df['name'].apply(lambda x: x.replace('_firstShootHitRate', ''))
        df_list.append(df)

df_all = pd.concat(df_list, axis=0, ignore_index=True)
df_all.columns = ['ID', 'firstShootRate']

# 保存合并后的DataFrame到文件
df_all.to_csv(output_file, index=False)

# 读取fin.csv文件和firstHitRate.csv文件
fin_df = pd.read_csv(input_file)
hit_rate_df = pd.read_csv(output_file)

# 合并数据
result_df = pd.merge(fin_df, hit_rate_df, on='ID', how='left')
result_df.fillna({'firstShootRate': 0}, inplace=True)

# 保存合并后的DataFrame到文件
result_df.to_csv(output_file1, index=False)
