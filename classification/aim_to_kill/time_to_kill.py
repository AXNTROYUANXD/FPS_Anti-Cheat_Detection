import csv
import os


def to_kill(path, id):
    # 获取所有作弊用户的ID
    try:
        # 打开对应的playerFrames文件
        playerFramesFile = open(f"{path}/{id}_playerFrames.csv", newline="")
        playerFramesReader = csv.DictReader(playerFramesFile)

        # 创建空字典来存储每个round已经被kill的victim
        roundVictims = {}

        # 遍历playerFrames文件中的每一行
        for row in playerFramesReader:
            # 如果spotters不为空
            if row["spotters"] != "[]":
                # 解析出victim的SteamID
                spotters = row["spotters"].strip("[]").split(",")
                for victimSteamID in spotters:
                    # 如果这个victim在当前round已经被kill过了，跳过这个victim
                    if (row["roundNum"], victimSteamID) in roundVictims:
                        continue

                    # 记录当前round和victim
                    roundNum = row["roundNum"]
                    see_tick = int(row["tick"])
                    victim = victimSteamID

                    # 打开对应的kills文件
                    killsFile = open(f"{path}/{id}_kills.csv", newline="")
                    killsReader = csv.DictReader(killsFile)

                    # 遍历kills文件中的每一行，找到第一个符合条件的kill
                    for killRow in killsReader:
                        if (killRow["attackerName"] == row["name"] and
                                killRow["roundNum"] == roundNum and
                                killRow["victimSteamID"] in spotters and
                                int(killRow["tick"]) <= see_tick + 1280):
                            kill_tick = int(killRow["tick"]) - see_tick
                            roundVictims[(roundNum, victim)] = True
                            # 将数据写入timeToKill文件
                            timeToKillFile = open(f"timeToKill/{id}_timeToKill.csv", "a", newline="")
                            timeToKillWriter = csv.writer(timeToKillFile)
                            timeToKillWriter.writerow(
                                [killRow["attackerName"], killRow["victimSteamID"], roundNum, kill_tick])
                            timeToKillFile.close()
                            break

                    killsFile.close()

        playerFramesFile.close()
        print("done " + id)
    except FileNotFoundError:
        print(f"文件 {id}_playerFrames.csv 不存在。跳过此cheaterID。")


if __name__ == '__main__':
    file_path = '/Volumes/T7/cheater_demos'
    subfolders = [f.path for f in os.scandir(file_path) if f.is_dir()]
    for s in subfolders:
        try:
            print(s)
            to_kill(s, s.split('/')[-1])
        except:
            pass
