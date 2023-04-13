import csv
import os


def flashStatGenerator(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if 'flashes.csv' in f:

                with open(root + '/' + 'flashStats.csv', mode='w', newline='', encoding='utf_8_sig') as file:
                    fieldnames = ['attackerName', 'flashThrown', 'tick', 'affectedEnemyCount', 'affectedEnemyDuration',
                                  'affectedEnemyEfficiency', 'affectedFriendlyCount', 'affectedFriendlyDuration',
                                  'affectedFriendlyDeficiency', 'affectedTotalDuration', 'flashEfficiencyInTotal']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                with open(os.path.join(root, f), mode='r', encoding="utf_8_sig") as Ffile:
                    reader = csv.DictReader(Ffile)
                    attacker_data = {}
                    for row in reader:

                        attacker_name = row['attackerName']
                        attacker_tick = row['tick']
                        attackerFinal = attacker_name + '@#@' + attacker_tick
                        attackerSide = row['attackerSide']
                        victimSide = row['playerSide']
                        flashDuration = row['flashDuration']

                        if attacker_name != '' or attacker_name != 'Gunner':
                            if attackerFinal not in attacker_data:
                                attacker_data[attackerFinal] = {'flashThrown': 0,
                                                                'tick': 0,
                                                                'affectedEnemyCount': 0,
                                                                'affectedEnemyDuration': 0.0,
                                                                'affectedEnemyEfficiency': 0.0,
                                                                'affectedFriendlyCount': 0,
                                                                'affectedFriendlyDuration': 0.0,
                                                                'affectedFriendlyDeficiency': 0.0,
                                                                'affectedTotalDuration': 0.0,
                                                                'flashEfficiencyInTotal': 0.0}

                            attacker_data[attackerFinal]['tick'] = attacker_tick
                            # Thrown once
                            attacker_data[attackerFinal]['flashThrown'] = 1

                            attacker_data[attackerFinal]['affectedTotalDuration'] += float(flashDuration)

                            # Friendly Flashed
                            if attackerSide == victimSide:
                                attacker_data[attackerFinal]['affectedFriendlyCount'] += 1
                                attacker_data[attackerFinal][
                                    'affectedFriendlyDuration'] += float(flashDuration)
                                # Enemy Flashed
                            else:
                                attacker_data[attackerFinal]['affectedEnemyCount'] += 1
                                attacker_data[attackerFinal]['affectedEnemyDuration'] += float(flashDuration)

                with open(root + '/' + 'flashStats.csv', mode='a', newline='',
                          encoding="utf_8_sig") as flash_file:
                    writer = csv.DictWriter(flash_file, fieldnames=fieldnames)
                    for attackerFinal, data in attacker_data.items():
                        if attackerFinal.split("@#@")[0] != 'Gunner':
                            flashThrown = data['flashThrown']
                            thrownTick = data['tick']
                            affectedEnemyCount = data['affectedEnemyCount']
                            affectedEnemyDuration = data['affectedEnemyDuration']
                            affectedFriendlyCount = data['affectedFriendlyCount']
                            affectedFriendlyDuration = data['affectedFriendlyDuration']
                            affectedTotalDuration = data['affectedTotalDuration']

                            # Calculating affectedEnemyEfficiency
                            affectedEnemyEfficiency = affectedEnemyDuration / affectedTotalDuration if affectedTotalDuration > 0 else 0
                            affectedFriendlyDeficiency = affectedFriendlyDuration / affectedTotalDuration if affectedTotalDuration > 0 else 0
                            flashEfficiencyInTotal = affectedEnemyEfficiency - affectedFriendlyDeficiency

                            writer.writerow({'attackerName': attackerFinal.split("@#@")[0], 'flashThrown': flashThrown,
                                             'tick': thrownTick,
                                             'affectedEnemyCount': affectedEnemyCount,
                                             'affectedEnemyDuration': affectedEnemyDuration,
                                             'affectedEnemyEfficiency': affectedEnemyEfficiency,
                                             'affectedFriendlyCount': affectedFriendlyCount,
                                             'affectedFriendlyDuration': affectedFriendlyDuration,
                                             'affectedFriendlyDeficiency': affectedFriendlyDeficiency,
                                             'affectedTotalDuration': affectedTotalDuration,
                                             'flashEfficiencyInTotal': flashEfficiencyInTotal})

                with open(root + '/' + 'flashStatsFinal.csv', mode='w', newline='', encoding='utf_8_sig') as file:
                    fieldnames = ['attackerName', 'flashThrown', 'affectedEnemyCount',
                                  'affectedEnemyDuration',
                                  'affectedEnemyEfficiency', 'affectedFriendlyCount',
                                  'affectedFriendlyDuration',
                                  'affectedFriendlyDeficiency', 'affectedTotalDuration',
                                  'flashEfficiencyInTotal']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                with open(root + '/' + 'flashStats.csv', mode='r', encoding="utf_8_sig") as Ffile:
                    reader = csv.DictReader(Ffile)
                    attacker_data = {}
                    for row in reader:

                        attacker_name = row['attackerName']
                        flashThrown = row['flashThrown']
                        affectedEnemyCount = row['affectedEnemyCount']
                        affectedEnemyDuration = row['affectedEnemyDuration']
                        affectedFriendlyCount = row['affectedFriendlyCount']
                        affectedFriendlyDuration = row['affectedFriendlyDuration']
                        affectedTotalDuration = row['affectedTotalDuration']

                        if attacker_name != '' or attacker_name != 'Gunner':
                            if attacker_name not in attacker_data:
                                attacker_data[attacker_name] = {'flashThrown': 0,
                                                                'affectedEnemyCount': 0,
                                                                'affectedEnemyDuration': 0.0,
                                                                'affectedEnemyEfficiency': 0.0,
                                                                'affectedFriendlyCount': 0,
                                                                'affectedFriendlyDuration': 0.0,
                                                                'affectedFriendlyDeficiency': 0.0,
                                                                'affectedTotalDuration': 0.0,
                                                                'flashEfficiencyInTotal': 0.0}

                            attacker_data[attacker_name]['flashThrown'] += int(flashThrown)
                            attacker_data[attacker_name]['affectedEnemyCount'] += int(affectedEnemyCount)
                            attacker_data[attacker_name]['affectedEnemyDuration'] += float(affectedEnemyDuration)
                            attacker_data[attacker_name]['affectedFriendlyCount'] += int(affectedFriendlyCount)
                            attacker_data[attacker_name]['affectedFriendlyDuration'] += float(affectedFriendlyDuration)
                            attacker_data[attacker_name]['affectedTotalDuration'] += float(affectedTotalDuration)

                with open(root + '/' + 'flashStatsFinal.csv', mode='a', newline='',
                          encoding="utf_8_sig") as flash_file:
                    writer = csv.DictWriter(flash_file, fieldnames=fieldnames)
                    for attacker_name, data in attacker_data.items():
                        if attacker_name != 'Gunner':
                            flashThrown = data['flashThrown']
                            affectedEnemyCount = data['affectedEnemyCount']
                            affectedEnemyDuration = data['affectedEnemyDuration']
                            affectedFriendlyCount = data['affectedFriendlyCount']
                            affectedFriendlyDuration = data['affectedFriendlyDuration']
                            affectedTotalDuration = data['affectedTotalDuration']

                            # Calculating affectedEnemyEfficiency
                            affectedEnemyEfficiency = affectedEnemyDuration / affectedTotalDuration if affectedTotalDuration > 0 else 0
                            affectedFriendlyDeficiency = affectedFriendlyDuration / affectedTotalDuration if affectedTotalDuration > 0 else 0
                            flashEfficiencyInTotal = affectedEnemyEfficiency - affectedFriendlyDeficiency

                            writer.writerow(
                                {'attackerName': attacker_name, 'flashThrown': flashThrown,
                                 'affectedEnemyCount': affectedEnemyCount,
                                 'affectedEnemyDuration': affectedEnemyDuration,
                                 'affectedEnemyEfficiency': affectedEnemyEfficiency,
                                 'affectedFriendlyCount': affectedFriendlyCount,
                                 'affectedFriendlyDuration': affectedFriendlyDuration,
                                 'affectedFriendlyDeficiency': affectedFriendlyDeficiency,
                                 'affectedTotalDuration': affectedTotalDuration,
                                 'flashEfficiencyInTotal': flashEfficiencyInTotal})


# flashStatGenerator(r'D:\CSGO_Aanlysis\demos\test')
