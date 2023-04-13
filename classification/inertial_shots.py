import os
import csv
import pandas as pd


def inertialShotGenerator(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if "kills" in f:
                with open(os.path.join(root, f), 'r', encoding="utf_8_sig") as kf:
                    reader = csv.DictReader(kf)
                    for row in reader:
                        kill_tick = row['tick']
                        kill_seconds = float(row['seconds'])

                        totalKills = 0

                        with open(os.path.join(root, f), 'r', encoding="utf_8_sig") as kf2:
                            reader2 = csv.DictReader(kf2)
                            for row2 in reader2:
                                if row2['attackerSteamID'] == row['attackerSteamID']:
                                    totalKills += 1
                                else:
                                    pass

                        for f2 in files:
                            if "weaponFires" in f2:
                                with open(os.path.join(root, f), 'r', encoding="utf_8_sig") as wf:
                                    reader3 = csv.DictReader(wf)
                                    found_row = None
                                    for row3 in reader3:
                                        # if row3['tick'] == kill_tick and row3['playerName'] == row['attackerName']:
                                        if row3['tick'] == kill_tick and row3['attackerName'] == row['attackerName']:
                                            found_row = row3
                                            break

                                    if found_row is not None:
                                        inertial_shot_time = 0
                                        for row4 in reader3:
                                            # TODO HERE                               ↓↓↓↓↓ 0.15 seconds threshold
                                            if row4['attackerName'] == row['attackerName'] and float(
                                                    row4['seconds']) - kill_seconds <= 0.15:
                                                inertial_shot_time += 1
                                                break
                                            else:
                                                inertial_shot_time = inertial_shot_time
                                                break
                                        output_file = root + '/' + 'inertial_shots.csv'
                                        headers = ['ID', 'inertialShotTime', 'totalKills',
                                                   'inertialShotPercentage']
                                        write_header = not os.path.exists(output_file)

                                        with open(output_file, 'a', newline='', encoding="utf_8_sig") as f4:
                                            writer = csv.DictWriter(f4, fieldnames=headers)
                                            if write_header:
                                                writer.writeheader()
                                            writer.writerow(
                                                {'ID': row['attackerName'],
                                                 'inertialShotTime': inertial_shot_time,
                                                 'totalKills': totalKills, 'inertialShotPercentage': ''})

                                        df = pd.read_csv(root + '/' + 'inertial_shots.csv')

                                        grouped = df.groupby('ID').agg(
                                            {'inertialShotTime': 'sum', 'totalKills': 'mean'})

                                        grouped['inertialShotPercentage'] = grouped['inertialShotTime'] / (
                                            grouped['totalKills'])

                                        final_df = pd.DataFrame(grouped)

                                        final_df.to_csv(root + '/' + 'inertial_shots_final.csv', encoding="utf_8_sig")
                                break
                break

# inertialShotGenerator(r"D:\CSGO_Aanlysis\demos\test")