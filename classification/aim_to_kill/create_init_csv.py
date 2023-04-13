import os

import pandas as pd


def init_time_to_kill(prefix):
    # 定义 path 文件夹的路径
    folder_path = fr"/Volumes/T7/cheater_demos"

    # 定义 timeToSwitch 文件夹的路径
    output_folder_path = "timeToKill"

    # 如果 timeToSwitch 文件夹不存在，创建该文件夹
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 遍历 path 文件夹下的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历所有的 weaponFires.csv 文件
        for file in files:
            if file.endswith("_weaponFires.csv"):
                # 获取作弊用户的 cheaterId
                cheater_id = file.replace("_weaponFires.csv", "")

                # 读取 weaponFires.csv 文件
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)

                # 对 weaponFires 数据进行处理，计算 timeToSwitch
                # 这里需要你根据具体的数据格式和计算方法来实现

                # 创建 timeToSwitch.csv 文件，并将处理后的数据写入该文件
                output_file_path = os.path.join(output_folder_path, f"{cheater_id}_timeToKill.csv")
                df_output = pd.DataFrame(
                    columns=["attackerName", "victimSteamID", "roundNum", "kill_tick"])
                df_output.to_csv(output_file_path, index=False)


if __name__ == '__main__':
    file_path = '/Volumes/T7/demos/Train'
    subfolders = [f.path for f in os.scandir(file_path) if f.is_dir()]
    for s in subfolders:
        try:
            init_time_to_kill(s.split('/')[-1])
        except:
            pass
