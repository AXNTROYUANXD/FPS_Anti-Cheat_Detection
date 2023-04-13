import pandas as pd
import os

# 找到所有的cheaterID
cheaterIDs = set()
for file in os.listdir("path"):
    if file.endswith("_firstshoot.csv"):
        cheaterIDs.add(file.split("_")[0])

# 遍历所有的cheaterID
for cheaterID in cheaterIDs:
    print("handling " + cheaterID)
    firstshoot_file = f"path/{cheaterID}_firstshoot.csv"
    damages_file = f"path/{cheaterID}_damages.csv"
    output_file = f"firstShootHitRate/{cheaterID}_firstShootHitRate.csv"

    # 读取firstshoot文件
    firstshoot_df = pd.read_csv(firstshoot_file)

    # 初始化hit和miss
    hit_dict = {name: 0 for name in firstshoot_df["playerName"]}
    miss_dict = {name: 0 for name in firstshoot_df["playerName"]}

    # 读取damages文件
    damages_df = pd.read_csv(damages_file)

    # 遍历firstshoot文件中的每一行
    for _, row in firstshoot_df.iterrows():
        name = row["playerName"]
        shooting_tick = row["tick"]

        # 在damages文件中查找
        hit_row = damages_df[(damages_df["attackerName"] == name) & (damages_df["tick"] == shooting_tick)]
        if len(hit_row) > 0:
            hit_dict[name] += 1
        else:
            miss_dict[name] += 1

    # 计算命中率
    hit_rate_dict = {name: hit_dict[name] / (hit_dict[name] + miss_dict[name]) for name in hit_dict}

    # 保存结果
    result_df = pd.DataFrame({"name": hit_dict.keys(),
                              "hit": hit_dict.values(),
                              "miss": miss_dict.values(),
                              "rate": hit_rate_dict.values()})
    result_df.to_csv(output_file, index=False)
