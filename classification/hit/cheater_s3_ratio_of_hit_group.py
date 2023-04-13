import csv
import os

import pandas as pd


# 将三种玩家数据整合在一个csv中 保留列名attackerSteamID，新加两列ratio, type
def create_body_data(file_path, new_damage_data_file):
    with open(new_damage_data_file, "w", newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["ID", "Chest", "Generic", "Head", "LeftArm", "LeftLeg", "Neck", "RightArm", "RightLeg",
             "Stomach", "isCheater"])  # attributes

    for cheater_file_name in os.listdir(file_path):
        if "_damages.csv" in cheater_file_name:  # 定位每一个damages文件
            cheater_name = cheater_file_name.split('_')[0]  # 获取cheaterID
            data = pd.read_csv(os.path.join(file_path, cheater_file_name))
            # 提取cheater自己的数据
            data1 = data[data['attackerName'] == cheater_name]  # 提取cheater自己的数据
            cheater_damage_data1 = data1[["attackerName", "hitGroup"]].copy()
            cheater_damage_data1["isCheater"] = True
            df1 = ratio_hit_part(cheater_damage_data1, True)
            df1.to_csv(new_damage_data_file, index=False, mode='a', header=False)

            # 提取正常玩家的数据
            data2 = data[data['attackerName'] != cheater_name]
            cheater_damage_data2 = data2[["attackerName", "hitGroup"]].copy()
            cheater_damage_data2["isCheater"] = False
            df2 = ratio_hit_part(cheater_damage_data2, False)
            df2.to_csv(new_damage_data_file, index=False, mode='a', header=False)


def ratio_hit_part(data, type1):
    data = data.drop(data[data["attackerName"].isnull()].index)
    IDs = data["attackerName"].unique()
    num = len(IDs)
    chest, generic, head, leftarm, leftleg, neck, rightarm, rightleg, stomach = [0] * num, [0] * num, [0] * num, [
        0] * num, [0] * num, [0] * num, [0] * num, [0] * num, [0] * num
    n = 0

    for ID in IDs:
        data_each = data[data["attackerName"] == ID]
        damage = len(data_each)  # the number of damage
        chest[n] = len(data_each[data_each["hitGroup"] == "Chest"]) / damage
        generic[n] = len(data_each[data_each["hitGroup"] == "Generic"]) / damage
        head[n] = len(data_each[data_each["hitGroup"] == "Head"]) / damage
        leftarm[n] = len(data_each[data_each["hitGroup"] == "LeftArm"]) / damage
        leftleg[n] = len(data_each[data_each["hitGroup"] == "LeftLeg"]) / damage
        neck[n] = len(data_each[data_each["hitGroup"] == "Neck"]) / damage
        rightarm[n] = len(data_each[data_each["hitGroup"] == "RightArm"]) / damage
        rightleg[n] = len(data_each[data_each["hitGroup"] == "RightLeg"]) / damage
        stomach[n] = len(data_each[data_each["hitGroup"] == "Stomach"]) / damage
        n = n + 1

    datas = {
        'ID': IDs,
        "Chest": chest,
        "Generic": generic,
        "Head": head,
        "LeftArm": leftarm,
        "LeftLeg": leftleg,
        "Neck": neck,
        "RightArm": rightarm,
        "RightLeg": rightleg,
        "Stomach": stomach,
        'isCheater': type1}

    df = pd.DataFrame(datas)

    return df


def main(data_path):
    subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]
    for s in subfolders:
        try:
            new_damage_data_file = fr"../data_to_combine/s3/{s.split('/')[-1]}_s3_hit_group.csv"
            # 创建新数据文件
            create_body_data(s, new_damage_data_file)

            # 去重
            data = pd.read_csv(new_damage_data_file)

            data = data.drop_duplicates(subset=['ID'], keep=False, inplace=False)
            data.to_csv(fr'../data_to_combine/s3/{s.split("/")[-1]}_去重后_cheater_s3_hit_group.csv', index=False,
                        encoding='utf-8-sig')
        except:
            pass
