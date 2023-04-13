import os
import csv

# 定义文件夹路径
folder_path = 'path'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):

    # 判断文件名是否以'_weaponFires.csv'结尾
    if not filename.endswith('_weaponFires.csv'):
        continue

    # 解析出cheaterId
    cheater_id = filename.split('_')[0]

    # 拼接playerFrames文件名
    frames_filename = cheater_id + '_playerFrames.csv'

    # 构造文件路径
    fires_filepath = os.path.join(folder_path, filename)
    frames_filepath = os.path.join(folder_path, frames_filename)

    # 判断playerFrames文件是否存在
    if not os.path.isfile(frames_filepath):
        continue

    # 创建timeToSwitch文件
    output_filename = cheater_id + '_timeToSwitch.csv'
    output_filepath = os.path.join('./timeToSwitch', output_filename)

    # 打开weaponFires文件
    with open(fires_filepath, 'r') as fires_file:
        fires_reader = csv.DictReader(fires_file)

        # 遍历所有行
        for row in fires_reader:

            # 只处理weaponClass不为Pistols的情况
            if row['weaponClass'] == 'Pistols':
                continue

            # 如果ammoInMagazine为0，记录该行数据
            if row['ammoInMagazine'] == '0':
                player_name = row['playerName']
                round_num = row['roundNum']
                start_tick = row['tick']
                weapon = row['weapon']

                # 打开playerFrames文件
                with open(frames_filepath, 'r') as frames_file:
                    frames_reader = csv.DictReader(frames_file)

                    # 遍历所有行
                    for line_num, line in enumerate(frames_reader):

                        # 如果是目标玩家，且时间与roundNum相符
                        if line['name'] == player_name and line['roundNum'] == round_num and line['tick'] == start_tick:
                            weapon_before = line['activeWeapon']

                            # 继续往下找，直到找到玩家更换武器的时刻
                            for next_line in frames_reader:
                                if next_line['name'] == player_name:
                                    if next_line['activeWeapon'] != weapon_before:
                                        weapon_after = next_line['activeWeapon']
                                        tick_change = int(next_line['tick']) - int(start_tick)
                                        if (tick_change >= 0) and (tick_change <= 1280):
                                            # 写入timeToSwitch文件
                                            with open(output_filepath,
                                                      'a', newline='') as output_file:
                                                output_writer = csv.writer(output_file)
                                                output_writer.writerow(
                                                    [player_name, round_num, weapon, weapon_after, start_tick,
                                                     tick_change])
                                                print("done" + output_filepath)

                                            # 继续寻找下一个ammoInMagazine为0的行
                                        break
                            break
