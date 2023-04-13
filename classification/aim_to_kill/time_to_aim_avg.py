# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Author  : SUN Chenxin
# @Time    : 27/2/2023 7:44 pm
# @File    : time_to_aim_avg.py
import os
import csv

cheater_data_path = "timeToAim/"
avg_time_to_kill_path = "timeToAim_avg/"

# create folder if it doesn't exist
if not os.path.exists(avg_time_to_kill_path):
    os.makedirs(avg_time_to_kill_path)

def process_csv_file(file_path):
    attacker_killticks = {}
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            shooting_name = row['shooting_name']
            shooting_tick = int(row['shooting_tick'])
            if shooting_name in attacker_killticks:
                # update existing attacker
                attacker_data = attacker_killticks[shooting_name]
                attacker_data['shooting_ticks'].append(shooting_tick)
                if shooting_tick > attacker_data['max_aimtick']:
                    attacker_data['max_aimtick'] = shooting_tick
                if shooting_tick < attacker_data['min_aimtick']:
                    attacker_data['min_aimtick'] = shooting_tick
            else:
                # add new attacker
                attacker_killticks[shooting_name] = {
                    'shooting_ticks': [shooting_tick],
                    'max_aimtick': shooting_tick,
                    'min_aimtick': shooting_tick
                }

    # write to csv file
    filename = os.path.basename(file_path)
    cheater_id = filename.split('_')[0]
    with open(avg_time_to_kill_path + cheater_id + '_avgtimeToAim.csv', mode='w', newline='') as csv_file:
        fieldnames = ['ID', 'avg_aimtick', 'max_aimtick', 'min_aimtick']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for shooting_name, attacker_data in attacker_killticks.items():
            avg_killtick = sum(attacker_data['shooting_ticks']) / len(attacker_data['shooting_ticks'])
            csv_writer.writerow({
                'ID': shooting_name,
                'avg_aimtick': avg_killtick,
                'max_aimtick': attacker_data['max_aimtick'],
                'min_aimtick': attacker_data['min_aimtick']
            })


# loop through all files in cheater path folder
for filename in os.listdir(cheater_data_path):
    if filename.endswith("_timeToAim.csv"):
        file_path = os.path.join(cheater_data_path, filename)
        process_csv_file(file_path)
