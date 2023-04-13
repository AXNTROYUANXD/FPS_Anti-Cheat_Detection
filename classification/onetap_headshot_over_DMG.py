import csv
import os


def shotEfficiencyGenerator(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if 'damages' in f:
                # Create hitEfficiency csv file
                with open(root + '/' + 'hitEfficiency.csv', mode='w', newline='',
                          encoding='utf_8_sig') as hitEfficiency_file:
                    fieldnames = ['ID', 'sniperShotted', 'less_50_snipershotted', '50_100_snipershotted',
                                  '100_200_sniperShotted', '200_500_snipershotted', '500_800_sniperShotted',
                                  '800_1000_sniperShotted', 'more_1000_sniperShotted', 'sniperHeadShotted',
                                  'less_50_sniperHeadShotted', '50_100_sniperHeadShotted',
                                  '100_200_sniperHeadShotted', '200_500_sniperHeadShotted', '500_800_sniperHeadShotted',
                                  '800_1000_sniperHeadShotted', 'more_1000_sniperHeadShotted',
                                  'sniperHeadPercentage',
                                  'normalShotted', 'less_50_normalShotted', '50_100_normalShotted',
                                  '100_200_normalShotted', '200_500_normalShotted', '500_800_normalShotted',
                                  '800_1000_normalShotted', 'more_1000_normalShotted', 'normalHeadShotted',
                                  'less_50_normalHeadShotted', '50_100_normalHeadShotted',
                                  '100_200_normalHeadShotted', '200_500_normalHeadShotted', '500_800_normalHeadShotted',
                                  '800_1000_normalHeadShotted', 'more_1000_normalHeadShotted', 'normalHeadPercentage',
                                  'oneTap', 'less_50_oneTap', '50_100_oneTap',
                                  '100_200_oneTap', '200_500_oneTap', '500_800_oneTap',
                                  '800_1000_oneTap', 'more_1000_oneTap', 'oneTapPercentage']
                    writer = csv.DictWriter(hitEfficiency_file, fieldnames=fieldnames)
                    writer.writeheader()

                # Process damages csv file and update hitEfficiency csv file
                with open(os.path.join(root, f), mode='r', encoding='utf_8_sig') as damages_file:
                    reader = csv.DictReader(damages_file)
                    attacker_data = {}
                    for row in reader:
                        attacker_name = row['attackerName']
                        if row['weapon'] in ['C4', 'World'] or row['attackerName'] in ['Gunner']:
                            continue
                        if row['weapon'] in ['SSG 08', 'AWP']:
                            if attacker_name not in attacker_data:
                                attacker_data[attacker_name] = {'sniperShotted': 0, 'less_50_snipershotted': 0,
                                                                '50_100_snipershotted': 0,
                                                                '100_200_sniperShotted': 0, '200_500_snipershotted': 0,
                                                                '500_800_sniperShotted': 0,
                                                                '800_1000_sniperShotted': 0,
                                                                'more_1000_sniperShotted': 0,
                                                                'sniperHeadShotted': 0, 'less_50_sniperHeadShotted': 0,
                                                                '50_100_sniperHeadShotted': 0,
                                                                '100_200_sniperHeadShotted': 0,
                                                                '200_500_sniperHeadShotted': 0,
                                                                '500_800_sniperHeadShotted': 0,
                                                                '800_1000_sniperHeadShotted': 0,
                                                                'more_1000_sniperHeadShotted': 0,
                                                                'normalShotted': 0, 'less_50_normalShotted': 0,
                                                                '50_100_normalShotted': 0,
                                                                '100_200_normalShotted': 0, '200_500_normalShotted': 0,
                                                                '500_800_normalShotted': 0,
                                                                '800_1000_normalShotted': 0,
                                                                'more_1000_normalShotted': 0,
                                                                'normalHeadShotted': 0, 'less_50_normalHeadShotted': 0,
                                                                '50_100_normalHeadShotted': 0,
                                                                '100_200_normalHeadShotted': 0,
                                                                '200_500_normalHeadShotted': 0,
                                                                '500_800_normalHeadShotted': 0,
                                                                '800_1000_normalHeadShotted': 0,
                                                                'more_1000_normalHeadShotted': 0,
                                                                'oneTap': 0, 'less_50_oneTap': 0, '50_100_oneTap': 0,
                                                                '100_200_oneTap': 0, '200_500_oneTap': 0,
                                                                '500_800_oneTap': 0,
                                                                '800_1000_oneTap': 0, 'more_1000_oneTap': 0}
                            attacker_data[attacker_name]['sniperShotted'] += 1
                            if float(row['distance']) <= 50.0:
                                attacker_data[attacker_name]['less_50_snipershotted'] += 1
                            if 50.0 < float(row['distance']) <= 100.0:
                                attacker_data[attacker_name]['50_100_snipershotted'] += 1
                            if 100.0 < float(row['distance']) <= 200.0:
                                attacker_data[attacker_name]['100_200_sniperShotted'] += 1
                            if 200.0 < float(row['distance']) <= 500.0:
                                attacker_data[attacker_name]['200_500_snipershotted'] += 1
                            if 500.0 < float(row['distance']) <= 800.0:
                                attacker_data[attacker_name]['500_800_sniperShotted'] += 1
                            if 800.0 < float(row['distance']) <= 1000.0:
                                attacker_data[attacker_name]['800_1000_sniperShotted'] += 1
                            if float(row['distance']) > 1000.0:
                                attacker_data[attacker_name]['more_1000_sniperShotted'] += 1

                            if row['hitGroup'] == 'Head':
                                attacker_data[attacker_name]['sniperHeadShotted'] += 1

                                if float(row['distance']) <= 50.0:
                                    attacker_data[attacker_name]['less_50_sniperHeadshotted'] += 1
                                if 50.0 < float(row['distance']) <= 100.0:
                                    attacker_data[attacker_name]['50_100_sniperHeadshotted'] += 1
                                if 100.0 < float(row['distance']) <= 200.0:
                                    attacker_data[attacker_name]['100_200_sniperHeadShotted'] += 1
                                if 200.0 < float(row['distance']) <= 500.0:
                                    attacker_data[attacker_name]['200_500_sniperHeadShotted'] += 1
                                if 500.0 < float(row['distance']) <= 800.0:
                                    attacker_data[attacker_name]['500_800_sniperHeadShotted'] += 1
                                if 800.0 < float(row['distance']) <= 1000.0:
                                    attacker_data[attacker_name]['800_1000_sniperHeadShotted'] += 1
                                if float(row['distance']) > 1000.0:
                                    attacker_data[attacker_name]['more_1000_sniperHeadShotted'] += 1
                        else:
                            if attacker_name not in attacker_data:
                                attacker_data[attacker_name] = {'sniperShotted': 0, 'less_50_snipershotted': 0,
                                                                '50_100_snipershotted': 0,
                                                                '100_200_sniperShotted': 0, '200_500_snipershotted': 0,
                                                                '500_800_sniperShotted': 0,
                                                                '800_1000_sniperShotted': 0,
                                                                'more_1000_sniperShotted': 0,
                                                                'sniperHeadShotted': 0, 'less_50_sniperHeadShotted': 0,
                                                                '50_100_sniperHeadShotted': 0,
                                                                '100_200_sniperHeadShotted': 0,
                                                                '200_500_sniperHeadShotted': 0,
                                                                '500_800_sniperHeadShotted': 0,
                                                                '800_1000_sniperHeadShotted': 0,
                                                                'more_1000_sniperHeadShotted': 0,
                                                                'normalShotted': 0, 'less_50_normalShotted': 0,
                                                                '50_100_normalShotted': 0,
                                                                '100_200_normalShotted': 0, '200_500_normalShotted': 0,
                                                                '500_800_normalShotted': 0,
                                                                '800_1000_normalShotted': 0,
                                                                'more_1000_normalShotted': 0,
                                                                'normalHeadShotted': 0, 'less_50_normalHeadShotted': 0,
                                                                '50_100_normalHeadShotted': 0,
                                                                '100_200_normalHeadShotted': 0,
                                                                '200_500_normalHeadShotted': 0,
                                                                '500_800_normalHeadShotted': 0,
                                                                '800_1000_normalHeadShotted': 0,
                                                                'more_1000_normalHeadShotted': 0,
                                                                'oneTap': 0, 'less_50_oneTap': 0, '50_100_oneTap': 0,
                                                                '100_200_oneTap': 0, '200_500_oneTap': 0,
                                                                '500_800_oneTap': 0,
                                                                '800_1000_oneTap': 0, 'more_1000_oneTap': 0}
                            attacker_data[attacker_name]['normalShotted'] += 1
                            if float(row['distance']) <= 50.0:
                                attacker_data[attacker_name]['less_50_normalShotted'] += 1
                            if 50.0 < float(row['distance']) <= 100.0:
                                attacker_data[attacker_name]['50_100_normalShotted'] += 1
                            if 100.0 < float(row['distance']) <= 200.0:
                                attacker_data[attacker_name]['100_200_normalShotted'] += 1
                            if 200.0 < float(row['distance']) <= 500.0:
                                attacker_data[attacker_name]['200_500_normalShotted'] += 1
                            if 500.0 < float(row['distance']) <= 800.0:
                                attacker_data[attacker_name]['500_800_normalShotted'] += 1
                            if 800.0 < float(row['distance']) <= 1000.0:
                                attacker_data[attacker_name]['800_1000_normalShotted'] += 1
                            if float(row['distance']) > 1000.0:
                                attacker_data[attacker_name]['more_1000_normalShotted'] += 1

                            if row['hitGroup'] == 'Head':
                                attacker_data[attacker_name]['normalHeadShotted'] += 1
                                if float(row['distance']) <= 50.0:
                                    attacker_data[attacker_name]['less_50_normalHeadShotted'] += 1
                                if 50.0 < float(row['distance']) <= 100.0:
                                    attacker_data[attacker_name]['50_100_normalHeadShotted'] += 1
                                if 100.0 < float(row['distance']) <= 200.0:
                                    attacker_data[attacker_name]['100_200_normalHeadShotted'] += 1
                                if 200.0 < float(row['distance']) <= 500.0:
                                    attacker_data[attacker_name]['200_500_normalHeadShotted'] += 1
                                if 500.0 < float(row['distance']) <= 800.0:
                                    attacker_data[attacker_name]['500_800_normalHeadShotted'] += 1
                                if 800.0 < float(row['distance']) <= 1000.0:
                                    attacker_data[attacker_name]['800_1000_normalHeadShotted'] += 1
                                if float(row['distance']) > 1000.0:
                                    attacker_data[attacker_name]['more_1000_normalHeadShotted'] += 1
                            if int(row['hpDamage']) >= 100:
                                attacker_data[attacker_name]['oneTap'] += 1
                                if float(row['distance']) <= 50.0:
                                    attacker_data[attacker_name]['less_50_oneTap'] += 1
                                if 50.0 < float(row['distance']) <= 100.0:
                                    attacker_data[attacker_name]['50_100_oneTap'] += 1
                                if 100.0 < float(row['distance']) <= 200.0:
                                    attacker_data[attacker_name]['100_200_oneTap'] += 1
                                if 200.0 < float(row['distance']) <= 500.0:
                                    attacker_data[attacker_name]['200_500_oneTap'] += 1
                                if 500.0 < float(row['distance']) <= 800.0:
                                    attacker_data[attacker_name]['500_800_oneTap'] += 1
                                if 800.0 < float(row['distance']) <= 1000.0:
                                    attacker_data[attacker_name]['800_1000_oneTap'] += 1
                                if float(row['distance']) > 1000.0:
                                    attacker_data[attacker_name]['more_1000_oneTap'] += 1

                # Calculate hit efficiency and update hitEfficiency csv file
                with open(root + '/' + 'hitEfficiency.csv', mode='a', newline='',
                          encoding='utf_8_sig') as hitEfficiency_file1:
                    writer = csv.DictWriter(hitEfficiency_file1, fieldnames=fieldnames)
                    for attacker_name, data in attacker_data.items():
                        sniper_shotted = data['sniperShotted']
                        sniper_head_shotted = data['sniperHeadShotted']
                        normal_shotted = data['normalShotted']
                        normal_head_shotted = data['normalHeadShotted']
                        one_tap = data['oneTap']
                        sniper_head_percentage = sniper_head_shotted / sniper_shotted if sniper_shotted > 0 else 0
                        normal_head_percentage = normal_head_shotted / normal_shotted if normal_shotted > 0 else 0
                        one_tap_percentage = one_tap / normal_shotted if normal_shotted > 0 else 0
                        writer.writerow({'ID': attacker_name, 'sniperShotted': sniper_shotted,
                                         'less_50_snipershotted': data['less_50_snipershotted'],
                                         '50_100_snipershotted': data['50_100_snipershotted'],
                                         '100_200_sniperShotted': data['100_200_sniperShotted'],
                                         '200_500_snipershotted': data['200_500_snipershotted'],
                                         '500_800_sniperShotted': data['500_800_sniperShotted'],
                                         '800_1000_sniperShotted': data['800_1000_sniperShotted'],
                                         'more_1000_sniperShotted': data['more_1000_sniperShotted'],
                                         'sniperHeadShotted': sniper_head_shotted,
                                         'less_50_sniperHeadShotted': data['less_50_sniperHeadShotted'],
                                         '50_100_sniperHeadShotted': data['50_100_sniperHeadShotted'],
                                         '100_200_sniperHeadShotted': data['100_200_sniperHeadShotted'],
                                         '200_500_sniperHeadShotted': data['200_500_sniperHeadShotted'],
                                         '500_800_sniperHeadShotted': data['500_800_sniperHeadShotted'],
                                         '800_1000_sniperHeadShotted': data['800_1000_sniperHeadShotted'],
                                         'more_1000_sniperHeadShotted': data['more_1000_sniperHeadShotted'],
                                         'sniperHeadPercentage': sniper_head_percentage,
                                         'normalShotted': normal_shotted,
                                         'less_50_normalShotted': data['less_50_normalShotted'],
                                         '50_100_normalShotted': data['50_100_normalShotted'],
                                         '100_200_normalShotted': data['100_200_normalShotted'],
                                         '200_500_normalShotted': data['200_500_normalShotted'],
                                         '500_800_normalShotted': data['500_800_normalShotted'],
                                         '800_1000_normalShotted': data['800_1000_normalShotted'],
                                         'more_1000_normalShotted': data['more_1000_normalShotted'],
                                         'normalHeadShotted': normal_head_shotted,
                                         'less_50_normalHeadShotted': data['less_50_normalHeadShotted'],
                                         '50_100_normalHeadShotted': data['50_100_normalHeadShotted'],
                                         '100_200_normalHeadShotted': data['100_200_normalHeadShotted'],
                                         '200_500_normalHeadShotted': data['200_500_normalHeadShotted'],
                                         '500_800_normalHeadShotted': data['500_800_normalHeadShotted'],
                                         '800_1000_normalHeadShotted': data['800_1000_normalHeadShotted'],
                                         'more_1000_normalHeadShotted': data['more_1000_normalHeadShotted'],
                                         'normalHeadPercentage': normal_head_percentage,
                                         'oneTap': one_tap, 'less_50_oneTap': data['less_50_oneTap'],
                                         '50_100_oneTap': data['50_100_oneTap'],
                                         '100_200_oneTap': data['100_200_oneTap'], '200_500_oneTap': data['200_500_oneTap'],
                                         '500_800_oneTap': data['500_800_oneTap'],
                                         '800_1000_oneTap': data['800_1000_oneTap'],
                                         'more_1000_oneTap': data['more_1000_oneTap'],
                                         'oneTapPercentage': one_tap_percentage})


# shotEfficiencyGenerator(r'D:\CSGO_Aanlysis\demos\test')
