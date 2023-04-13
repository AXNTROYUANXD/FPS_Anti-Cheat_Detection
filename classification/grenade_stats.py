import os
import csv


def totalRounds(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if 'grenades.csv' in f:
                total_rounds = 0
                with open(os.path.join(root, f), mode='r', encoding="utf_8_sig") as Rfile:
                    reader = csv.DictReader(Rfile)
                    for row in reader:
                        currentRound = row['roundNum']
                        total_rounds = currentRound
    return total_rounds


def grenadeStats(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            if 'grenades.csv' in f:
                with open(root + '/' + 'grenadeStats.csv', mode='w', newline='', encoding='utf_8_sig') as file:
                    fieldnames = ['attackerName', 'totalRound', 'Incendiary_Molotov', 'Incendiary_Molotov_per_round',
                                  'avg_Incendiary_Molotov_per_round', 'total_Incendiary_Molotov',
                                  'Flashbang', 'Flashbang_per_round', 'avg_Flashbang_per_round', 'total_Flashbang',
                                  'HE Grenade', 'HE Grenade_per_round', 'avg_HE Grenade_per_round', 'total_HE Grenade',
                                  'Smoke Grenade',
                                  'Smoke Grenade_per_round', 'avg_Smoke Grenade_per_round', 'total_Smoke Grenade',
                                  'IM_Applied_Rate', 'FB_Applied_Rate', 'HE_Applied_Rate', 'SMK_Applied_Rate']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                total_Incendiary_Molotov = 0
                total_Flashbang = 0
                totoal_HE_Grenade = 0
                total_Smoke_Grenade = 0

                with open(os.path.join(root, f), mode='r', encoding="utf_8_sig") as Gfile:
                    reader = csv.DictReader(Gfile)
                    attacker_data = {}

                    for row in reader:

                        attacker_name = row['throwerName']
                        grenade_type = row['grenadeType']

                        if attacker_name != '':
                            if attacker_name not in attacker_data:
                                attacker_data[attacker_name] = {'totalRound': 0, 'Incendiary_Molotov': 0,
                                                                'Incendiary_Molotov_per_round': 0.0,
                                                                'avg_Incendiary_Molotov_per_round': 0.0,
                                                                'total_Incendiary_Molotov': 0,
                                                                'Flashbang': 0, 'Flashbang_per_round': 0.0,
                                                                'avg_Flashbang_per_round': 0.0, 'total_Flashbang': 0,
                                                                'HE Grenade': 0, 'HE Grenade_per_round': 0.0,
                                                                'avg_HE Grenade_per_round': 0.0, 'total_HE Grenade': 0,
                                                                'Smoke Grenade': 0, 'Smoke Grenade_per_round': 0.0,
                                                                'avg_Smoke Grenade_per_round': 0.0,
                                                                'total_Smoke Grenade': 0, 'IM_Applied_Rate': 0.0,
                                                                'FB_Applied_Rate': 0.0, 'HE_Applied_Rate': 0.0,
                                                                'SMK_Applied_Rate': 0.0}
                            if grenade_type == 'Incendiary Grenade' or grenade_type == 'Molotov':
                                attacker_data[attacker_name]['Incendiary_Molotov'] += 1
                                total_Incendiary_Molotov += 1
                            if grenade_type == 'Flashbang':
                                attacker_data[attacker_name]['Flashbang'] += 1
                                total_Flashbang += 1
                            if grenade_type == 'HE Grenade':
                                attacker_data[attacker_name]['HE Grenade'] += 1
                                totoal_HE_Grenade += 1
                            if grenade_type == 'Smoke Grenade':
                                attacker_data[attacker_name]['Smoke Grenade'] += 1
                                total_Smoke_Grenade += 1

                total_rounds = totalRounds(root)

                with open(root + '/' + 'grenadeStats.csv', mode='a', newline='',
                          encoding="utf_8_sig") as grenades_file:
                    writer = csv.DictWriter(grenades_file, fieldnames=fieldnames)
                    for attacker_name, data in attacker_data.items():
                        IM = data['Incendiary_Molotov']
                        FB = data['Flashbang']
                        HE = data['HE Grenade']
                        SMK = data['Smoke Grenade']

                        total_IM = total_Incendiary_Molotov
                        total_FB = total_Flashbang
                        total_HE = totoal_HE_Grenade
                        total_SMK = total_Smoke_Grenade

                        IM_PR = IM / int(total_rounds)
                        FB_PR = FB / int(total_rounds)
                        HE_PR = HE / int(total_rounds)
                        SMK_PR = SMK / int(total_rounds)

                        avg_IM_PR = total_IM / int(total_rounds)
                        avg_FB_PR = total_FB / int(total_rounds)
                        avg_HE_PR = total_HE / int(total_rounds)
                        avg_SMK_PR = total_SMK / int(total_rounds)

                        IM_A_R = IM / total_IM
                        FB_A_R = FB / total_FB
                        HE_A_R = HE / total_HE
                        SMK_A_R = SMK / total_SMK

                        writer.writerow(
                            {'attackerName': attacker_name, 'totalRound': total_rounds, 'Incendiary_Molotov': IM,
                             'Incendiary_Molotov_per_round': IM_PR,
                             'avg_Incendiary_Molotov_per_round': avg_IM_PR, 'total_Incendiary_Molotov': total_IM,
                             'Flashbang': FB, 'Flashbang_per_round': FB_PR, 'avg_Flashbang_per_round': avg_FB_PR,
                             'total_Flashbang': total_FB,
                             'HE Grenade': HE, 'HE Grenade_per_round': HE_PR, 'avg_HE Grenade_per_round': avg_HE_PR,
                             'total_HE Grenade': total_HE,
                             'Smoke Grenade': SMK,
                             'Smoke Grenade_per_round': SMK_PR, 'avg_Smoke Grenade_per_round': avg_SMK_PR,
                             'total_Smoke Grenade': total_SMK, 'IM_Applied_Rate': IM_A_R,
                                                                'FB_Applied_Rate': FB_A_R, 'HE_Applied_Rate': HE_A_R,
                                                                'SMK_Applied_Rate': SMK_A_R})


# grenadeStats(r'D:\CSGO_Aanlysis\demos\test')
