import os
import csv


def get_cheater_data(file_path):
    cheater_data = {}
    for file_name in os.listdir(file_path):
        if '_weaponFires.csv' in file_name:
            cheater_id = file_name.split('_')[0]
            cheater_data[cheater_id] = {
                'weaponFires': os.path.join(file_path, file_name),
                'playerFrames': os.path.join(file_path, f'{cheater_id}_playerFrames.csv')
            }
    return cheater_data


def get_time_to_aim(cheater_data):
    for cheater_id, files in cheater_data.items():
        weapon_fires_path = files['weaponFires']
        player_frames_path = files['playerFrames']
        output_path = f'timeToAim/{cheater_id}_timeToAim.csv'

        with open(weapon_fires_path) as weapon_fires_file, open(player_frames_path) as player_frames_file, open(
                output_path, 'w', newline='') as output_file:
            weapon_fires_reader = csv.DictReader(weapon_fires_file)
            player_frames_reader = csv.DictReader(player_frames_file)
            writer = csv.DictWriter(output_file, fieldnames=['shooting_name', 'round', 'aiming_tick'])
            writer.writeheader()

            for shooting_data in weapon_fires_reader:
                shooting_name = shooting_data['playerName']
                round_num = shooting_data['roundNum']
                shooting_tick = shooting_data['tick']


                aiming_tick = None

                for player_data in player_frames_reader:
                    if player_data['name'] != shooting_name or player_data['roundNum'] != round_num:
                        continue
                    if player_data['tick'] > shooting_tick:
                        break
                    if player_data['spotters'] == '[]':
                        continue
                    aiming_tick = int(shooting_tick) - int(player_data['tick'])
                    for prev_player_data in player_frames_reader:
                        if prev_player_data['name'] != shooting_name or prev_player_data['roundNum'] != round_num:
                            break
                        if prev_player_data['tick'] <= player_data['tick']:
                            break
                        if prev_player_data['spotters'] == '[]':
                            break
                        aiming_tick = int(shooting_tick) - int(prev_player_data['tick'])
                    break

                if aiming_tick is None or aiming_tick < 0 or aiming_tick > 640:
                    continue

                writer.writerow({
                    'shooting_name': shooting_name,
                    'round': round_num,
                    'aiming_tick': aiming_tick
                })

                # reset player frames reader
                player_frames_file.seek(0)
                next(player_frames_reader)
                next(player_frames_reader)


def process_file(weapon_fires_file, player_frames_file, time_to_aim_file):
    # 读取 weaponFires 文件，记录每个射击事件的信息
    with open(weapon_fires_file, 'r') as wf:
        wf_reader = csv.DictReader(wf)
        last_round_num = None
        last_name = None
        for wf_row in wf_reader:
            shooting_name = wf_row['playerName']
            round_num = wf_row['roundNum']
            shooting_tick = int(wf_row['tick'])
            if shooting_name == last_name and round_num == last_round_num:
                continue
            last_name = shooting_name
            last_round_num = round_num

            # 在 playerFrames 文件中查找 spotters
            with open(player_frames_file, 'r') as pf:
                pf_reader = csv.DictReader(pf)
                aiming_tick = None
                for pf_row in pf_reader:
                    name = pf_row['name']
                    pf_round_num = pf_row['roundNum']
                    tick = int(pf_row['tick'])
                    spotters = pf_row['spotters']
                    if name == shooting_name and pf_round_num == round_num and tick == shooting_tick:
                        # 找到当前射击事件对应的行
                        if spotters == '[]':
                            # 如果 spotters 为空，则退出当前循环，处理下一个射击事件
                            break
                        else:
                            # 否则往上找到第一个 spotters 为空的行，记录 aiming_tick
                            for pf_row2 in pf_reader:
                                if pf_row2['name'] == name and pf_row2['roundNum'] == pf_round_num and pf_row2[
                                    'spotters'] == '[]':
                                    aiming_tick = int(pf_row2['tick'])
                                    break
                            break

                # 如果 aiming_tick 不为空，则将射击事件的信息保存到 time_to_aim 文件中
                if aiming_tick is not None:
                    aiming_tick -= shooting_tick
                    if aiming_tick >= 0 and aiming_tick <= 640:
                        with open(time_to_aim_file, 'a', newline='') as ta:
                            ta_writer = csv.writer(ta)
                            ta_writer.writerow([shooting_name, round_num, aiming_tick])

                # 跳过下两行
                for i in range(2):
                    try:
                        next(wf_reader)
                    except StopIteration:
                        break


def main():
    # 设置数据文件夹路径
    data_dir = './cheaterdataAim'

    # 遍历数据文件夹中的所有文件
    for filename in os.listdir(data_dir):
        # 如果是weaponFires文件，则处理该文件
        if filename.endswith('_weaponFires.csv'):
            cheater_id = filename.split('_')[0]
            weapon_fires_file = os.path.join(data_dir, filename)
            player_frames_file = os.path.join(data_dir, f'{cheater_id}_playerFrames.csv')
            time_to_aim_file = os.path.join('./timeToAim', f'{cheater_id}_timeToAim.csv')
            process_file(weapon_fires_file, player_frames_file, time_to_aim_file)
            print("done " + filename)


if __name__ == '__main__':
    main()
