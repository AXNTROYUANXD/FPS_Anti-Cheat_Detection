# -*- coding: utf-8 -*-
# !/usr/bin/python3
# @Author  : SUN Chenxin
# @Time    : 27/2/2023 7:44 pm
# @File    : time_to_kill_avg.py
import os
import csv

cheater_data_path = "timeToKill/"
avg_time_to_kill_path = "timeToKill_avg/"

# create folder if it doesn't exist
if not os.path.exists(avg_time_to_kill_path):
    os.makedirs(avg_time_to_kill_path)

def process_csv_file(file_path):
    attacker_killticks = {}
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            attackerName = row['attackerName']
            kill_tick = int(row['kill_tick'])
            if attackerName in attacker_killticks:
                # update existing attacker
                attacker_data = attacker_killticks[attackerName]
                attacker_data['kill_tick'].append(kill_tick)
                if kill_tick > attacker_data['max_killtick']:
                    attacker_data['max_killtick'] = kill_tick
                if kill_tick < attacker_data['min_killtick']:
                    attacker_data['min_killtick'] = kill_tick
            else:
                # add new attacker
                attacker_killticks[attackerName] = {
                    'kill_tick': [kill_tick],
                    'max_killtick': kill_tick,
                    'min_killtick': kill_tick
                }

    # write to csv file
    filename = os.path.basename(file_path)
    cheater_id = filename.split('_')[0]
    with open(avg_time_to_kill_path + cheater_id + '_avgtimeToKill.csv', mode='w', newline='') as csv_file:
        fieldnames = ['ID', 'avg_killtick', 'max_killtick', 'min_killtick']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for attackerName, attacker_data in attacker_killticks.items():
            avg_killtick = sum(attacker_data['kill_tick']) / len(attacker_data['kill_tick'])
            csv_writer.writerow({
                'ID': attackerName,
                'avg_killtick': avg_killtick,
                'max_killtick': attacker_data['max_killtick'],
                'min_killtick': attacker_data['min_killtick']
            })


# loop through all files in cheater path folder
for filename in os.listdir(cheater_data_path):
    if filename.endswith("_timeToKill.csv"):
        file_path = os.path.join(cheater_data_path, filename)
        process_csv_file(file_path)
