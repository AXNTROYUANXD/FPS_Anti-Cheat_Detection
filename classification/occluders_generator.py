import os
import csv


def occluderGenerator(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if 'kills.csv' in f:
                # Create a new CSV file for occluders data
                with open(root + '/' + 'occluders.csv', mode='w', newline='', encoding='utf_8_sig') as file:
                    fieldnames = ['attackerName', 'onePenetrationWallBangTime', 'twoPenetrationsWallBangTime',
                                  'manyPenetrationsWallBangTime', 'firstKillTime', 'blindedKillTime',
                                  'noScopeKillTime', 'thruSmokeKillTime']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                # Open the kills CSV file and read the data row by row
                with open(os.path.join(root, f), mode='r', encoding="utf_8_sig") as Kfile:
                    reader = csv.DictReader(Kfile)
                    attacker_data = {}
                    for row in reader:

                        attacker_name = row['attackerName']
                        is_wallbang = row['isWallbang']
                        penetrated_objects = row['penetratedObjects']
                        is_first_kill = row['isFirstKill']
                        attacker_blinded = row['attackerBlinded']
                        no_scope = row['noScope']
                        thru_smoke = row['thruSmoke']

                        if attacker_name != '':
                            if attacker_name not in attacker_data:
                                attacker_data[attacker_name] = {'onePenetrationWallBangTime': 0,
                                                                'twoPenetrationsWallBangTime': 0,
                                                                'manyPenetrationsWallBangTime': 0, 'firstKillTime': 0,
                                                                'blindedKillTime': 0,
                                                                'noScopeKillTime': 0, 'thruSmokeKillTime': 0}
                            if is_wallbang:
                                if int(penetrated_objects) == 1:
                                    attacker_data[attacker_name]['onePenetrationWallBangTime'] += 1
                                if int(penetrated_objects) == 2:
                                    attacker_data[attacker_name]['twoPenetrationsWallBangTime'] += 1
                                if int(penetrated_objects) > 2:
                                    attacker_data[attacker_name]['manyPenetrationsWallBangTime'] += 1
                            if is_first_kill == 'True':
                                attacker_data[attacker_name]['firstKillTime'] += 1
                            if attacker_blinded== 'True':
                                attacker_data[attacker_name]['blindedKillTime'] += 1
                            if no_scope == 'True':
                                attacker_data[attacker_name]['noScopeKillTime'] += 1
                            if thru_smoke == 'True':
                                attacker_data[attacker_name]['thruSmokeKillTime'] += 1

                # Write the updated row back to the occluders CSV file
                with open(root + '/' + 'occluders.csv', mode='a', newline='',
                          encoding="utf_8_sig") as occluders_file:
                    writer = csv.DictWriter(occluders_file, fieldnames=fieldnames)
                    for attacker_name, data in attacker_data.items():
                        onePenetrationWallBangTime = data['onePenetrationWallBangTime']
                        twoPenetrationsWallBangTime = data['twoPenetrationsWallBangTime']
                        manyPenetrationsWallBangTime = data['manyPenetrationsWallBangTime']
                        first_kill_time = data['firstKillTime']
                        attacker_blinded_kill_time = data['blindedKillTime']
                        no_scope_kill_time = data['noScopeKillTime']
                        thru_smoke_kill_time = data['thruSmokeKillTime']

                        writer.writerow({'attackerName': attacker_name,
                                         'onePenetrationWallBangTime': onePenetrationWallBangTime,
                                         'twoPenetrationsWallBangTime': twoPenetrationsWallBangTime,
                                         'manyPenetrationsWallBangTime': manyPenetrationsWallBangTime,
                                         'firstKillTime': first_kill_time,
                                         'blindedKillTime': attacker_blinded_kill_time,
                                         'noScopeKillTime': no_scope_kill_time,
                                         'thruSmokeKillTime': thru_smoke_kill_time})


# occluderGenerator(r'D:\CSGO_Aanlysis\demos\test')
