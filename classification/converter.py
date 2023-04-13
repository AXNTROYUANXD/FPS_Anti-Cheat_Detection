import csv
import os

import pandas as pd


def convert2oneInFolder(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if '.csv' in f:
                # 输入文件夹路径和输出文件路径
                folder_path = root
                output_file = root + "TestFinal.csv"

                # 获取文件夹内所有 CSV 文件的文件名
                csv_files = ["hitEfficiency.csv", "inertial_shots_final.csv", "occluders.csv", "flashStatsFinal.csv",
                             "grenadeStats.csv"
                             ]

                # 用字典存储每个第一列内容相同的行，并把剩余列存储在一个列表中
                rows_dict = {}
                headers = {}
                for file in csv_files:
                    try:
                        with open(os.path.join(folder_path, file), 'r', encoding="utf_8_sig") as f1:
                            reader = csv.reader(f1)
                            headers[file] = next(reader)  # 存储 CSV 文件的表头
                            for row in reader:
                                key = row[0]
                                if key not in rows_dict:
                                    rows_dict[key] = [[] for _ in range(len(csv_files))]
                                rows_dict[key][csv_files.index(file)] = row[1:]
                    except:
                        pass
                # 拆分每个 CSV 文件的表头并添加到新文件
                new_headers = []
                for file in csv_files:
                    try:
                        new_headers.extend([header for header in headers[file][1:]])
                    except:
                        pass
                # 写入 CSV 文件
                with open(output_file, 'w', newline='', encoding="utf_8_sig") as f2:
                    writer = csv.writer(f2)
                    writer.writerow(["ID"] + new_headers + ["isCheater"])  # 写入新的表头
                    for key, values in rows_dict.items():

                        # 将所有行合并成一个列表
                        if root.split('\\')[-1] == str(key):
                            row = [key] + [val for sublist in values for val in sublist]
                        else:
                            row = [key] + [val for sublist in values for val in sublist]

                        writer.writerow(row)

                # 读取CSV文件
                df = pd.read_csv(output_file, encoding="utf_8_sig")

                # 遍历每行数据
                for index, row in df.iterrows():
                    # 获取第一个值
                    first_value = row[0]

                    # 判断第一个值是否为SDASD
                    if first_value == root.split('/')[-1]:
                        # 在isCheater列填入True
                        df.at[index, 'isCheater'] = True
                    else:
                        # 在isCheater列填入False
                        df.at[index, 'isCheater'] = False

                # 将更新后的数据写入CSV文件
                df.to_csv(output_file, index=False, encoding="utf_8_sig")


def convert2One(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # 创建 Final.csv 文件并写入表头
        with open(os.path.join(root, 'Final.csv'), mode='w', newline='', encoding="utf_8_sig") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["ID", "sniperShotted", "less_50_snipershotted", "50_100_snipershotted", "100_200_sniperShotted",
                 "200_500_snipershotted", "500_800_sniperShotted", "800_1000_sniperShotted", "more_1000_sniperShotted",
                 "sniperHeadShotted", "less_50_sniperHeadShotted", "50_100_sniperHeadShotted",
                 "100_200_sniperHeadShotted",
                 "200_500_sniperHeadShotted", "500_800_sniperHeadShotted", "800_1000_sniperHeadShotted",
                 "more_1000_sniperHeadShotted", "sniperHeadPercentage", "normalShotted", "less_50_normalShotted",
                 "50_100_normalShotted", "100_200_normalShotted", "200_500_normalShotted", "500_800_normalShotted",
                 "800_1000_normalShotted", "more_1000_normalShotted", "normalHeadShotted", "less_50_normalHeadShotted",
                 "50_100_normalHeadShotted", "100_200_normalHeadShotted", "200_500_normalHeadShotted",
                 "500_800_normalHeadShotted", "800_1000_normalHeadShotted", "more_1000_normalHeadShotted",
                 "normalHeadPercentage", "oneTap", "less_50_oneTap", "50_100_oneTap", "100_200_oneTap",
                 "200_500_oneTap",
                 "500_800_oneTap", "800_1000_oneTap", "more_1000_oneTap", "oneTapPercentage", "inertialShotTime",
                 "totalKills", "inertialShotPercentage", "onePenetrationWallBangTime", "twoPenetrationsWallBangTime",
                 "manyPenetrationsWallBangTime", "firstKillTime", "blindedKillTime", "noScopeKillTime",
                 "thruSmokeKillTime",
                 "totalRound", "Incendiary_Molotov", "Incendiary_Molotov_per_round", "avg_Incendiary_Molotov_per_round",
                 "total_Incendiary_Molotov", "Flashbang", "Flashbang_per_round", "avg_Flashbang_per_round",
                 "total_Flashbang", "HE Grenade", "HE Grenade_per_round", "avg_HE Grenade_per_round",
                 "total_HE Grenade",
                 "Smoke Grenade", "Smoke Grenade_per_round", "avg_Smoke Grenade_per_round", "total_Smoke Grenade",
                 "IM_Applied_Rate", "FB_Applied_Rate", "HE_Applied_Rate", "SMK_Applied_Rate", "flashThrown",
                 "affectedEnemyCount", "affectedEnemyDuration", "affectedEnemyEfficiency", "affectedFriendlyCount",
                 "affectedFriendlyDuration", "affectedFriendlyDeficiency", "affectedTotalDuration",
                 "flashEfficiencyInTotal", "isCheater"])
        for f in files:
            if 'TestFinal.csv' in f:

                with open(os.path.join(root, f), mode='r', encoding="utf_8_sig") as file:
                    reader = csv.reader(file)
                    next(reader)  # 跳过表头

                    # 将每一行数据添加到 Final.csv 文件中
                    with open(os.path.join(root, 'Final.csv'), mode='a', newline='',
                              encoding="utf_8_sig") as final_file:
                        writer = csv.writer(final_file)
                        for row in reader:
                            # 如果某一列的值为空，则填充为0
                            row = [0 if value == '' else value for value in row]
                            writer.writerow(row)


def eliminateDuplicates(file_dir):
    for root, dirs, files in os.walk(file_dir):
        df = pd.read_csv(os.path.join(root, 'Final.csv'), encoding="utf_8_sig")
        df = df.drop_duplicates(subset='ID', keep=False)
        df.to_csv(os.path.join(root, 'Final.csv'), encoding="utf_8_sig", index=False)


def convertEverything(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # 读取三个csv文件
        df1 = pd.read_csv(root + '/' + 'FINAL_GY.csv', encoding="utf_8_sig")
        df2 = pd.read_csv(root + '/' + 'FINAL_SCX.csv', encoding="utf_8_sig")
        df3 = pd.read_csv(root + '/' + 'FINAL_ZJY.csv', encoding="utf_8_sig")

        # 合并三个DataFrame
        merged_df = pd.merge(df1, df2, on="ID", how="outer")
        merged_df = pd.merge(merged_df, df3, on="ID", how="outer")
        merged_df.to_csv(root + '/' + "FINAL.csv", index=False, encoding="utf_8_sig")


# convert2oneInFolder(r"D:\CSGO_Aanlysis\demos\test\cheat")
# convert2One(r"D:\CSGO_Aanlysis\demos\test\cheat")
# eliminateDuplicates(r"D:\CSGO_Aanlysis\demos\test\cheat")
convertEverything(r'C:\Users\bruce\Desktop\FINAL')
