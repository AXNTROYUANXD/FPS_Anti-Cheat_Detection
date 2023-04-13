import fnmatch
import os

import pandas as pd

s1_cols = ["ID", "damage distance", "isCheater"]
s2_cols = ["ID", "ratio of hit when moving", "isCheater"]
s3_cols = ["ID", "Chest", "Generic", "Head", "LeftArm", "LeftLeg", "Neck", "RightArm", "RightLeg", "Stomach",
           "isCheater"]
s4_cols = ["ID", "precision", "isCheater"]

pd.set_option('display.width', 10000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


def sub_combine(path, col):
    os.mkdir(path)
    l_path = f'./{path}/'
    files = sorted(os.listdir(l_path))

    data = [','.join(col) + '\n']
    for fn in files:
        if fnmatch.fnmatch(fn, '*去重*'):
            with open(l_path + fn, 'r') as file:
                data.extend(
                    [x for x in file.readlines()[1:]])

    with open(f'../data_to_combine/{path}.csv', 'w') as f:
        f.writelines(data)


def combine():
    path = '../data_to_combine'
    df_s1 = pd.read_csv(f'{path}/s1.csv', usecols=s1_cols)
    df_s1 = df_s1.drop_duplicates(subset=['ID'])

    df_s2 = pd.read_csv(f'{path}/s2.csv', usecols=s2_cols)
    df_s2 = df_s2.drop_duplicates(subset=['ID'])

    df_s3 = pd.read_csv(f'{path}/s3.csv', usecols=s3_cols)
    df_s3 = df_s3.drop_duplicates(subset=['ID'])

    df_s4 = pd.read_csv(f'{path}/s4.csv', usecols=s4_cols)
    df_s4 = df_s4.drop_duplicates(subset=['ID'])

    df = pd.merge(df_s1, df_s2, how='inner', on='ID')
    df = pd.merge(df, df_s3, how='inner', on='ID')
    df = pd.merge(df, df_s4, how='inner', on='ID')

    df.to_csv('data_to_combine/hit_fin_data.csv')


def main():
    sub_combine('s1', s1_cols)
    sub_combine('s2', s2_cols)
    sub_combine('s3', s3_cols)
    sub_combine('s4', s4_cols)
    combine()
