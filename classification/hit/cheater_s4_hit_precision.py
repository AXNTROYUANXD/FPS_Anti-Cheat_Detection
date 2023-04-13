import csv
import os

import pandas as pd


# 将三种玩家数据整合在一个csv中 保留列名playerSteamID, 新加两列precision, type
def create_fire_data(file_path, new_fire_data_file):
    with open(new_fire_data_file, "w", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "precision", "isCheater"])  # attributes

    for cheater_file_name in os.listdir(file_path):
        if "_weaponFires.csv" in cheater_file_name:
            cheater_name = cheater_file_name.split('_')[0]  # 获取cheaterID
            data = pd.read_csv(os.path.join(file_path, cheater_file_name))

            # 提取cheater自己的数据
            data1 = data[data['playerName'] == cheater_name]
            cheater_fire_data1 = data1[["playerName", "tick"]].copy()
            cheater_fire_data1["damage"] = False
            cheater_fire_data1["isCheater"] = True
            # 普通玩家
            data3 = data[data['playerName'] != cheater_name]
            cheater_fire_data2 = data3[["playerName", "tick"]].copy()
            cheater_fire_data2["damage"] = False
            cheater_fire_data2["isCheater"] = False

            fire_file_name = cheater_file_name[:-16] + "_damages.csv"
            for cheater_file_name in os.listdir(file_path):
                if cheater_file_name == fire_file_name:
                    # cheater数据
                    data2 = pd.read_csv(os.path.join(file_path, cheater_file_name))
                    cheater_damage_data1 = data2[["attackerName", "tick"]].copy()
                    for index, row in cheater_damage_data1.iterrows():
                        # 在fire中查找是否有同样的行数据
                        matching_rows1 = cheater_fire_data1[
                            (cheater_fire_data1['playerName'] == row['attackerName']) & (
                                    cheater_fire_data1['tick'] == row['tick'])]
                        if not matching_rows1.empty:
                            # 如果找到匹配的行数据，则将对应行的damage标为True
                            cheater_fire_data1.loc[matching_rows1.index, 'damage'] = True
                    df1 = hit_precision(cheater_fire_data1, True)
                    df1.to_csv(new_fire_data_file, index=False, mode='a', header=False)

                    # 普通玩家
                    data4 = pd.read_csv(os.path.join(file_path, cheater_file_name))
                    cheater_damage_data2 = data4[["attackerName", "tick"]].copy()
                    for index, row in cheater_damage_data2.iterrows():
                        # 在fire中查找是否有同样的行数据
                        matching_rows2 = cheater_fire_data2[
                            (cheater_fire_data2['playerName'] == row['attackerName']) & (
                                    cheater_fire_data2['tick'] == row['tick'])]
                        if not matching_rows2.empty:
                            # 如果找到匹配的行数据，则将对应行的damage标为True
                            cheater_fire_data2.loc[matching_rows2.index, 'damage'] = True

                    df2 = hit_precision(cheater_fire_data2, False)
                    df2.to_csv(new_fire_data_file, index=False, mode='a', header=False)


def hit_precision(data, type1):
    data = data.drop(data[data["playerName"].isnull()].index)
    IDs = data["playerName"].unique()
    num = len(IDs)
    precision = [0] * num
    n = 0

    for ID in IDs:
        data_each = data[data["playerName"] == ID]
        fire = len(data_each)
        damage = len(data_each[data_each["damage"] == True])
        precision[n] = damage / fire
        n = n + 1

    datas = {
        'ID': IDs,
        'precision': precision,
        'isCheater': type1}

    df = pd.DataFrame(datas)

    return df


def main(data_path):
    subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]
    for s in subfolders:
        try:
            new_damage_data_file = fr"../data_to_combine/s4/{s.split('/')[-1]}_s4_hit_precision.csv"
            # 创建新数据文件
            create_fire_data(s, new_damage_data_file)

            # 去重
            data = pd.read_csv(new_damage_data_file)

            data = data.drop_duplicates(subset=['ID'], keep=False, inplace=False)
            data.to_csv(fr'../data_to_combine/s4/{s.split("/")[-1]}_去重后_cheater_s4_hit_precision.csv', index=False,
                        encoding='utf-8-sig')
        except:
            pass
