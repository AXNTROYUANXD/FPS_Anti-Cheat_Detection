import csv
import os

import pandas as pd


# 将三种玩家数据整合在一个csv中 保留列名attackerSteamID,新加两列ratio, type
def create_damage_data(file_path, new_damage_data_file):
    with open(new_damage_data_file, "w", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "ratio of hit when moving", "isCheater"])  # attributes

    for cheater_file_name in os.listdir(file_path):
        if "_damages.csv" in cheater_file_name:  # 定位每一个damages文件
            data = pd.read_csv(os.path.join(file_path, cheater_file_name))
            cheater_name = cheater_file_name.split('_')[0]  # 获取cheaterID
            # 提取cheater自己的数据
            data1 = data[data['attackerName'] == cheater_name]
            cheater_damage_data1 = data1[["attackerName", "attackerStrafe"]].copy()
            cheater_damage_data1["type"] = True
            df1 = ratio_hit_move(cheater_damage_data1, True)
            df1.to_csv(new_damage_data_file, index=False, mode='a', header=False)
            # 提取正常玩家的数据
            data2 = data[data['attackerName'] != cheater_name]
            cheater_damage_data2 = data2[["attackerName", "attackerStrafe"]].copy()
            cheater_damage_data2["type"] = False
            df2 = ratio_hit_move(cheater_damage_data2, False)
            df2.to_csv(new_damage_data_file, index=False, mode='a', header=False)


def ratio_hit_move(data, type1):
    data = data.drop(data[data["attackerName"].isnull()].index)
    IDs = data["attackerName"].unique()
    num = len(IDs)
    ratio = [0] * num
    n = 0

    for ID in IDs:
        data_each = data[data["attackerName"] == ID]
        hit = len(data_each)  # the number of hit
        if hit == 0:
            ratio[n] = 0
            n = n + 1
            continue
        move = len(data_each[data_each["attackerStrafe"]])
        # ratio.append(move/hit)
        ratio[n] = move / hit
        n = n + 1

    datas = {
        'ID': IDs,
        'ratio': ratio,
        'isCheater': type1}

    df = pd.DataFrame(datas)
    return df


def main(data_path):
    subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]
    for s in subfolders:
        try:
            new_damage_data_file = fr"../data_to_combine/s2/{s.split('/')[-1]}_s2_hit_when_moving.csv"
            # 创建新数据文件
            create_damage_data(s, new_damage_data_file)

            # 去重
            data = pd.read_csv(new_damage_data_file)

            data = data.drop_duplicates(subset=['ID'], keep=False, inplace=False)
            data.to_csv(fr'./s2/{s.split("/")[-1]}_去重后_cheater_s2_hit_when_moving.csv', index=False,
                        encoding='utf-8-sig')
        except:
            pass
