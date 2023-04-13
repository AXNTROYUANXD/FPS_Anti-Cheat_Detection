import json
import math
import os
import traceback
from typing import Any

import numpy as np
import pandas as pd

pd.set_option('display.width', 10000)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# column
round_num = 'roundNum'
tick = 'tick'
seconds = 'seconds'
steam_id = 'steamID'
name = 'name'
view_x = 'viewX'
view_y = 'viewY'
spotters = 'spotters'

attacker_steam_id = 'attackerSteamID'
attacker_view_x = 'attackerViewX'
attacker_view_y = 'attackerViewY'
victim_steam_id = 'victimSteamID'

frame_cols = [round_num, tick, seconds, steam_id, name, view_x, view_y, spotters]
fire_cols = [tick, seconds, 'playerSteamID', 'playerName', 'playerViewX', 'playerViewY']
damage_cols = [tick, seconds, attacker_steam_id, 'attackerName', attacker_view_x, attacker_view_y, victim_steam_id]

# const
max_decimal_num = 6
server_tick = 128
fire_duration_tick = server_tick
fire_reaction_tick = server_tick / 2
result_data_path = 'angle_data'


class PlayerData:
    def __init__(self, sid: str, player_name: str, frames: pd.DataFrame,
                 fires: pd.DataFrame, damages: pd.DataFrame) -> None:
        self.id = str(sid)
        self.name = player_name
        self.frames = frames
        self.fires = fires
        self.damages = damages


# TODO: 方差 variance


def get_degree(x: float, y: float) -> float:
    degree = np.rad2deg(np.arctan(y / x))
    return round(degree, max_decimal_num)


def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2)


def get_speed(distance: float, duration: float) -> float:
    if duration != 0:
        return distance / duration
    return 999


def load_data(data_path, file_prefix: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # TODO: 路径要改！
    frame_data = f'{os.path.join(data_path, file_prefix)}_playerFrames.csv'
    print(os.path.join(data_path, file_prefix))
    fire_data = f'{os.path.join(data_path, file_prefix)}_weaponFires.csv'
    damage_data = f'{os.path.join(data_path, file_prefix)}_damages.csv'

    df_frame = pd.read_csv(frame_data, usecols=frame_cols)
    df_frame = df_frame[df_frame[spotters] != '[]'].reset_index(drop=True)

    df_fire = pd.read_csv(fire_data, usecols=fire_cols)
    df_fire.rename(columns={'playerSteamID': steam_id, 'playerName': name,
                            'playerViewX': view_x, 'playerViewY': view_y}, inplace=True)

    df_damage = pd.read_csv(damage_data, usecols=damage_cols)

    return df_frame, df_fire, df_damage


def get_players_data(frames: pd.DataFrame, fires: pd.DataFrame, damages: pd.DataFrame) -> list[PlayerData]:
    players_data = []
    ids = frames[steam_id].drop_duplicates().values

    for i in ids:
        # 按玩家steam id分类
        player_frames = frames[frames[steam_id] == i].reset_index(drop=True)
        # 提取df的第一行数据
        player_name = player_frames[name].iloc[0]
        player_fires = fires[fires[steam_id] == i].reset_index(drop=True)
        player_damages = damages[damages[attacker_steam_id] == i].reset_index(drop=True)

        player_data = PlayerData(str(i), player_name, player_frames, player_fires, player_damages)
        players_data.append(player_data)

    return players_data


def analyze_player_data(player_data: PlayerData) -> pd.DataFrame:
    # 遍历frame
    cols = ['steam_id', 'name', 'frame_tick', 'fire_tick', 'damage_tick', 'delta', 'gamma',
            't0_t1_duration', 't1_t2_duration', 'duration', 'speed']
    df = pd.DataFrame(columns=cols)

    print(f'Analyzing: {player_data.id}, {player_data.name}')

    last_victim_id = ''
    last_damage_tick = -1
    last_fire_tick = -1
    last_frame_tick = -1

    for dmg in player_data.damages.iterrows():
        dmg_data = dmg[1]
        victim_id = str(int(dmg_data[victim_steam_id]))

        if victim_id == last_victim_id:
            # 如果攻击目标和上次相同，但是间隔不超过1.5 * server_tick
            if dmg_data[tick] < (last_damage_tick + 1.5 * server_tick):
                continue
        last_victim_id = victim_id
        dmg_tick = dmg_data[tick]
        last_damage_tick = dmg_tick
        dmg_x = dmg_data[attacker_view_x]
        dmg_y = dmg_data[attacker_view_y]

        fr = player_data.fires[(player_data.fires[tick] <= dmg_tick) &
                               (player_data.fires[tick] >= (dmg_tick - fire_duration_tick * 1.5))]
        if fr.empty:
            fr = player_data.fires[(player_data.fires[tick] <= dmg_tick) &
                                   (player_data.fires[tick] >= (dmg_tick - fire_duration_tick * 1.75))]
            if fr.empty:
                continue
        most_recent_fire = fr.iloc[0]
        fr_tick = most_recent_fire[tick]
        if fr_tick == last_fire_tick:
            continue
        last_fire_tick = fr_tick
        fr_x = most_recent_fire[view_x]
        fr_y = most_recent_fire[view_y]

        t1_t2_duration = (dmg_tick - fr_tick) / server_tick

        for frm in player_data.frames[(player_data.frames[tick] >=
                                       max(last_frame_tick, fr_tick - fire_reaction_tick * 0.625)) &
                                      (player_data.frames[tick] <= fr_tick)].iterrows():
            frm_data = frm[1]
            frm_sps = [str(i) for i in json.loads(frm_data[spotters])]
            if victim_id not in frm_sps:
                continue

            frm_tick = frm_data[tick]
            if (frm_tick == last_frame_tick) or ((dmg_tick - frm_tick) >= (server_tick * 5)):
                break
            last_frame_tick = frm_tick
            frm_x = frm_data[view_x]
            frm_y = frm_data[view_y]

            t0_t1_duration = (fr_tick - frm_tick) / server_tick

            duration = (dmg_tick - frm_tick) / server_tick
            delta = 0
            try:
                delta = abs(get_degree(fr_x, fr_y) - get_degree(frm_x, frm_y))
            except Exception as e:
                print(traceback.print_exc())
                continue
            gamma = 0
            try:
                gamma = abs(get_degree(dmg_x, dmg_y) - get_degree(fr_x, fr_y))
            except Exception as e:
                print(traceback.print_exc())
                continue

            df.loc[len(df)] = [player_data.id, player_data.name, frm_tick, fr_tick, dmg_tick,
                               delta,
                               gamma, t0_t1_duration, t1_t2_duration,
                               duration, get_speed(get_distance(frm_x, frm_y, dmg_x, dmg_y), duration)]
            break
    print(df)
    return df


def summarize_player_data(p_data: pd.DataFrame) -> list[Any]:
    val = [
        str(int(p_data['steam_id'].iloc[0])),
        p_data['ID'].iloc[0],
        p_data['delta'].mean(),
        p_data['delta'].max(),
        p_data['delta'].min(),
        p_data['gamma'].mean(),
        p_data['gamma'].max(),
        p_data['gamma'].min(),

        p_data['t0_t1_duration'].mean(),
        p_data['t0_t1_duration'].max(),
        p_data['t0_t1_duration'].min(),

        p_data['t1_t2_duration'].mean(),
        p_data['t1_t2_duration'].max(),
        p_data['t1_t2_duration'].min(),

        p_data['duration'].mean(),
        p_data['duration'].max(),
        p_data['duration'].min(),
        p_data['speed'].mean(),
        p_data['speed'].max(),
        p_data['speed'].min(),
    ]
    return val


def generate_angle_duration_velocity_data(data_path, file_prefix: str) -> None:
    df_frame, df_fire, df_damage = load_data(data_path, file_prefix)
    players_data = get_players_data(df_frame, df_fire, df_damage)

    cols = ['steam_id', 'ID', 'avg_delta', 'max_delta', 'min_delta', 'avg_gamma', 'max_gamma', 'min_gamma',
            'avg_t0_t1_duration', 'max_t0_t1_duration', 'min_t0_t1_duration',
            'avg_t1_t2_duration', 'max_t1_t2_duration', 'min_t1_t2_duration',
            'avg_duration', 'max_duration', 'min_duration', 'avg_speed', 'max_speed', 'min_speed']
    df = pd.DataFrame(columns=cols)

    # 按玩家计算
    for p_data in players_data:
        apd = analyze_player_data(p_data)
        if apd.empty:
            continue
        val = summarize_player_data(apd)
        df.loc[len(df)] = val

    print(df)
    df.to_csv(os.path.join(result_data_path, file_prefix.split('/')[-1] + '_angle_duration_velocity.csv'),
              encoding='utf_8_sig', mode='w')


def main(data_path: str) -> None:
    os.mkdir(f'classification/{result_data_path}')
    subfolders = [f.path for f in os.scandir(data_path) if f.is_dir()]
    for s in subfolders:
        try:
            generate_angle_duration_velocity_data(data_path, s + '/' + s.split('/')[-1])
        except:
            print(traceback.print_exc())

    cols = ["steam_id", "ID", "avg_delta", "max_delta", "min_delta", "avg_gamma", "max_gamma", "min_gamma",
            "avg_t0_t1_duration", "max_t0_t1_duration", "min_t0_t1_duration",
            "avg_t1_t2_duration", "max_t1_t2_duration", "min_t1_t2_duration",
            "avg_duration", "max_duration", "min_duration",
            "avg_speed", "max_speed", "min_speed"]

    files = sorted(os.listdir(f'./{result_data_path}/'))

    data = [',' + ','.join(cols) + '\n']
    for fn in files:
        with open(result_data_path + fn, 'r') as file:
            data.extend(file.readlines()[1:])

    with open(f'data_to_combine/angle_fin_data.csv', 'w') as f:
        f.writelines(data)
