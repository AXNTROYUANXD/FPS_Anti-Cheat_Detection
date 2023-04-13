import os

import numpy as np
import pandas as pd
from keras import layers
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras


def find_processed_folders(file_dir):
    eco_folders = []
    engagement_folders = []
    movement_folders = []
    for root, dirs, files in os.walk(file_dir):
        for cur_dir in dirs:
            if '_Economy' in cur_dir:
                eco_folders.append(os.path.join(root, cur_dir))
            elif '_Engagement' in cur_dir:
                engagement_folders.append(os.path.join(root, cur_dir))
            elif '_Movement' in cur_dir:
                movement_folders.append(os.path.join(root, cur_dir))

    return eco_folders, engagement_folders, movement_folders


def read_single_csv(file):
    df = pd.read_csv(file, low_memory=False)
    return df


def read_folder_with_one_file(folder):
    file = os.listdir(folder)
    for file_name in file:
        df = read_single_csv(os.path.join(folder, file_name))
    return df


def good_data_name_list_in_each_folder(folder_path):
    # Candidates
    name = []
    # Filter out the incomplete data
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        num_files = len(os.listdir(subfolder_path))
        if '_Economy' in subfolder:
            if num_files == 1:
                name.append(subfolder[:subfolder.rfind('_')])
            else:
                continue
        elif '_Movement' in subfolder:
            if num_files == 1:
                name.append(subfolder[:subfolder.rfind('_')])
            else:
                continue
        elif '_Engagement' in subfolder:
            if num_files == 5:
                name.append(subfolder[:subfolder.rfind('_')])
            else:
                continue

    # Calculate each name duplicated times
    counts = {}
    for s in name:
        counts[s] = counts.get(s, 0) + 1

    # Filter out the bad data
    results = []
    for s in name:
        if counts[s] == 3:
            if s not in results:
                results.append(s)
        else:
            pass

    return results


def extract_df(name, path):
    economy_file = os.listdir(os.path.join(path, name + '_Economy'))[0]
    economy_df = pd.read_csv(os.path.join(os.path.join(path, name + '_Economy'), economy_file))
    movement_file = os.listdir(os.path.join(path, name + '_Movement'))[0]
    movement_df = pd.read_csv(os.path.join(os.path.join(path, name + '_Movement'), movement_file))
    engagement_path = os.listdir(os.path.join(path, name + '_Engagement'))
    damages_path = os.path.join(os.path.join(path, name + '_Engagement'), [file for file in engagement_path if
                                                                           '_damages_Processed.csv' in file][
        0])
    flashes_path = os.path.join(os.path.join(path, name + '_Engagement'), [file for file in engagement_path if
                                                                           '_flashes_Processed.csv' in file][
        0])
    grenades_path = os.path.join(os.path.join(path, name + '_Engagement'), [file for file in engagement_path if
                                                                            '_grenades_Processed.csv' in file][
        0])

    kills_path = os.path.join(os.path.join(path, name + '_Engagement'), [file for file in engagement_path if
                                                                         '_Kills_Processed.csv' in file][
        0])
    weapon_fires_path = os.path.join(os.path.join(path, name + '_Engagement'), [file for file in engagement_path if
                                                                                '_weaponFires_Processed.csv' in file][
        0])
    damages_df = pd.read_csv(damages_path)
    flashes_df = pd.read_csv(flashes_path)
    grenades_df = pd.read_csv(grenades_path)
    kills_df = pd.read_csv(kills_path)
    weapon_fires_df = pd.read_csv(weapon_fires_path)

    return economy_df, movement_df, damages_df, flashes_df, grenades_df, kills_df, weapon_fires_df


def eco_preprocess(df, time_step):
    df = df.drop(
        columns=["tick", "steamID", "name", "hasBomb", "hasHelmet", "hasDefuse"])
    df.set_index('roundNum', inplace=True)
    scaler = MinMaxScaler()
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def movement_preprocess(df, time_step):
    df = df.drop(
        columns=["roundNum", "side", "steamID", "name"])
    df.set_index('tick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def engagement_dmg_preprocess(df, time_step):
    df = df.drop(
        columns=["attackerSteamID", "attackerName", "victimSteamID"])
    df.set_index('tick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def engagement_flash_preprocess(df, time_step):
    df = df.drop(
        columns=["attackerSteamID", "attackerName", "playerSteamID"])
    df.set_index('tick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def engagement_grenade_preprocess(df, time_step):
    df = df.drop(
        columns=["throwerSteamID", "throwerName"])
    df.set_index('throwTick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def engagement_kill_preprocess(df, time_step):
    df = df.drop(
        columns=["attackerSteamID", "attackerName", "victimSteamID", "flashThrowerSteamID", "flashThrowerName",
                 "flashThrowerTeam"])
    df.set_index('tick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def engagement_weaponFire_preprocess(df, time_step):
    df = df.drop(
        columns=["playerSteamID", "playerName"])
    df.set_index('tick', inplace=True)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    x = scaler.fit_transform(df.drop(columns=["isCheater"]))
    # Pad x to have a length that is a multiple of time_step
    padding_width = time_step - x.shape[0] % time_step
    if padding_width < time_step:
        x = np.pad(x, ((0, padding_width), (0, 0)), mode="constant", constant_values=0)
    # Reshape x to have shape (num_samples, time_step, num_features)
    x = x.reshape(-1, time_step, x.shape[-1])
    y = df["isCheater"].values[:x.shape[0]]
    return x, y


def construct_eco_model(economy_df_x):
    eco_input = keras.Input(shape=(None, economy_df_x.shape[-1]), name="Economy Input")
    eco_features = layers.LSTM(128, return_sequences=True)(eco_input)
    eco_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(eco_features)
    eco_features = layers.LSTM(32, dropout=0.25)(eco_features)
    eco_pred = layers.Dense(1, activation="sigmoid", name="Economy_Prediction")(eco_features)

    model = keras.Model(
        inputs=[eco_input],
        outputs=[eco_pred], )
    model.summary()
    return model


def construct_movement_model(movement_df_x):
    movement_input = keras.Input(shape=(None, movement_df_x.shape[-1]), name="Movement Input")
    movement_features = layers.LSTM(256, return_sequences=True)(movement_input)
    movement_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(movement_features)
    movement_features = layers.LSTM(64, dropout=0.25)(movement_features)
    movement_pred = layers.Dense(1, activation="sigmoid", name="Movement_Prediction")(movement_features)

    model = keras.Model(
        inputs=[movement_input],
        outputs=[movement_pred], )
    model.summary()
    return model


def construct_engagement_dmg_model(damages_df_x):
    engagement_dmg_input = keras.Input(shape=(None, damages_df_x.shape[-1]), name="Engagement_DMGs Input")
    engagement_dmg_features = layers.LSTM(256, return_sequences=True)(engagement_dmg_input)
    engagement_dmg_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_dmg_features)
    engagement_dmg_features = layers.LSTM(64, dropout=0.25)(engagement_dmg_features)
    engagement_dmg_pred = layers.Dense(1, activation="sigmoid", name="Engagement_DMGs_Prediction")(
        engagement_dmg_features)

    model = keras.Model(
        inputs=[engagement_dmg_input],
        outputs=[engagement_dmg_pred], )
    model.summary()
    return model


def construct_engagement_flash_model(flashes_df_x):
    engagement_flash_input = keras.Input(shape=(None, flashes_df_x.shape[-1]), name="Engagement_FLASHES Input")
    engagement_flash_features = layers.LSTM(128, return_sequences=True)(engagement_flash_input)
    engagement_flash_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(engagement_flash_features)
    engagement_flash_features = layers.LSTM(32, dropout=0.25)(engagement_flash_features)
    engagement_flash_pred = layers.Dense(1, activation="sigmoid", name="Engagement_FLASHES_Prediction")(
        engagement_flash_features)

    model = keras.Model(
        inputs=[engagement_flash_input],
        outputs=[engagement_flash_pred], )
    model.summary()
    return model


def construct_engagement_grenade_model(grenades_df_x):
    engagement_grenade_input = keras.Input(shape=(None, grenades_df_x.shape[-1]), name="Engagement_GRENADES Input")
    engagement_grenade_features = layers.LSTM(128, return_sequences=True)(engagement_grenade_input)
    engagement_grenade_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(engagement_grenade_features)
    engagement_grenade_features = layers.LSTM(32, dropout=0.25)(engagement_grenade_features)
    engagement_grenade_pred = layers.Dense(1, activation="sigmoid", name="Engagement_GRENADES_Prediction")(
        engagement_grenade_features)

    model = keras.Model(
        inputs=[engagement_grenade_input],
        outputs=[engagement_grenade_pred], )
    model.summary()
    return model


def construct_engagement_kill_model(kills_df_x):
    engagement_kill_input = keras.Input(shape=(None, kills_df_x.shape[-1]), name="Engagement_KILLS Input")
    engagement_kill_features = layers.LSTM(256, return_sequences=True)(engagement_kill_input)
    engagement_kill_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_kill_features)
    engagement_kill_features = layers.LSTM(64, dropout=0.25)(engagement_kill_features)
    engagement_kill_pred = layers.Dense(1, activation="sigmoid", name="Engagement_KILLS_Prediction")(
        engagement_kill_features)

    model = keras.Model(
        inputs=[engagement_kill_input],
        outputs=[engagement_kill_pred], )
    model.summary()
    return model


def construct_engagement_weaponFire_model(weapon_fires_df_x):
    engagement_wf_input = keras.Input(shape=(None, weapon_fires_df_x.shape[-1]), name="Engagement_WEAPONFIRES Input")
    engagement_wf_features = layers.LSTM(256, return_sequences=True)(engagement_wf_input)
    engagement_wf_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_wf_features)
    engagement_wf_features = layers.LSTM(64, dropout=0.25)(engagement_wf_features)
    engagement_wf_pred = layers.Dense(1, activation="sigmoid", name="Engagement_WEAPONFIRES_Prediction")(
        engagement_wf_features)

    model = keras.Model(
        inputs=[engagement_wf_input],
        outputs=[engagement_wf_pred], )
    model.summary()
    return model


def construct_model(economy_df_x, movement_df_x, damages_df_x, flashes_df_x, grenades_df_x, kills_df_x,
                    weapon_fires_df_x):
    eco_input = keras.Input(shape=(None, economy_df_x.shape[-1]), name="Economy Input")
    movement_input = keras.Input(shape=(None, movement_df_x.shape[-1]), name="Movement Input")
    engagement_dmg_input = keras.Input(shape=(None, damages_df_x.shape[-1]), name="Engagement_DMGs Input")
    engagement_flash_input = keras.Input(shape=(None, flashes_df_x.shape[-1]), name="Engagement_FLASHES Input")
    engagement_grenade_input = keras.Input(shape=(None, grenades_df_x.shape[-1]), name="Engagement_GRENADES Input")
    engagement_kill_input = keras.Input(shape=(None, kills_df_x.shape[-1]), name="Engagement_KILLS Input")
    engagement_wf_input = keras.Input(shape=(None, weapon_fires_df_x.shape[-1]), name="Engagement_WEAPONFIRES Input")

    eco_features = layers.LSTM(128, return_sequences=True)(eco_input)
    eco_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(eco_features)
    eco_features = layers.LSTM(32, dropout=0.25)(eco_features)
    eco_pred = layers.Dense(1, activation="sigmoid", name="Economy_Prediction")(eco_features)
    # eco_pred_flatten = layers.Flatten()(eco_pred)
    # eco_pred_final = layers.Dense(1)(eco_pred_flatten)

    movement_features = layers.LSTM(256, return_sequences=True)(movement_input)
    movement_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(movement_features)
    movement_features = layers.LSTM(64, dropout=0.25)(movement_features)
    movement_pred = layers.Dense(1, activation="sigmoid", name="Movement_Prediction")(movement_features)
    # movement_pred_flatten = layers.Flatten()(movement_pred)
    # movement_pred_final = layers.Dense(1)(movement_pred_flatten)

    engagement_dmg_features = layers.LSTM(256, return_sequences=True)(engagement_dmg_input)
    engagement_dmg_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_dmg_features)
    engagement_dmg_features = layers.LSTM(64, dropout=0.25)(engagement_dmg_features)
    engagement_dmg_pred = layers.Dense(1, activation="sigmoid", name="Engagement_DMGs_Prediction")(
        engagement_dmg_features)
    # engagement_dmg_flatten = layers.Flatten()(engagement_dmg_pred)
    # engagement_dmg_pred_final = layers.Dense(1)(engagement_dmg_flatten)

    engagement_flash_features = layers.LSTM(128, return_sequences=True)(engagement_flash_input)
    engagement_flash_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(engagement_flash_features)
    engagement_flash_features = layers.LSTM(32, dropout=0.25)(engagement_flash_features)
    engagement_flash_pred = layers.Dense(1, activation="sigmoid", name="Engagement_FLASHES_Prediction")(
        engagement_flash_features)
    # engagement_flash_flatten = layers.Flatten()(engagement_flash_pred)
    # engagement_flash_pred_final = layers.Dense(1)(engagement_flash_flatten)

    engagement_grenade_features = layers.LSTM(128, return_sequences=True)(engagement_grenade_input)
    engagement_grenade_features = layers.LSTM(64, dropout=0.2, return_sequences=True)(engagement_grenade_features)
    engagement_grenade_features = layers.LSTM(32, dropout=0.25)(engagement_grenade_features)
    engagement_grenade_pred = layers.Dense(1, activation="sigmoid", name="Engagement_GRENADES_Prediction")(
        engagement_grenade_features)
    # engagement_grenade_flatten = layers.Flatten()(engagement_grenade_pred)
    # engagement_grenade_pred_final = layers.Dense(1)(engagement_grenade_flatten)

    engagement_kill_features = layers.LSTM(256, return_sequences=True)(engagement_kill_input)
    engagement_kill_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_kill_features)
    engagement_kill_features = layers.LSTM(64, dropout=0.25)(engagement_kill_features)
    engagement_kill_pred = layers.Dense(1, activation="sigmoid", name="Engagement_KILLS_Prediction")(
        engagement_kill_features)
    # engagement_kill_flatten = layers.Flatten()(engagement_kill_pred)
    # engagement_kill_pred_final = layers.Dense(1)(engagement_kill_flatten)

    engagement_wf_features = layers.LSTM(256, return_sequences=True)(engagement_wf_input)
    engagement_wf_features = layers.LSTM(128, dropout=0.2, return_sequences=True)(engagement_wf_features)
    engagement_wf_features = layers.LSTM(64, dropout=0.25)(engagement_wf_features)
    engagement_wf_pred = layers.Dense(1, activation="sigmoid", name="Engagement_WEAPONFIRES_Prediction")(
        engagement_wf_features)
    # engagement_wf_flatten = layers.Flatten()(engagement_wf_pred)
    # engagement_wf_pred_final = layers.Dense(1)(engagement_wf_flatten)

    # concatenate_all = layers.concatenate(
    #     [eco_pred_final, movement_pred_final, engagement_dmg_pred_final, engagement_flash_pred_final,
    #      engagement_grenade_pred_final, engagement_kill_pred_final, engagement_wf_pred_final])
    #
    # isCheater_pred = layers.Dense(1, activation="sigmoid", name="isCheater")(concatenate_all)

    # model = keras.Model(
    #     inputs=[eco_input, movement_input, engagement_dmg_input, engagement_flash_input, engagement_grenade_input,
    #             engagement_kill_input, engagement_wf_input],
    #     outputs=[eco_pred_final, movement_pred_final, engagement_dmg_pred_final, engagement_flash_pred_final,
    #              engagement_grenade_pred_final, engagement_kill_pred_final, engagement_wf_pred_final], )

    model = keras.Model(
        inputs=[eco_input, movement_input, engagement_dmg_input, engagement_flash_input, engagement_grenade_input,
                engagement_kill_input, engagement_wf_input],
        outputs=[eco_pred, movement_pred, engagement_dmg_pred, engagement_flash_pred,
                 engagement_grenade_pred, engagement_kill_pred, engagement_wf_pred], )

    model.summary()
    keras.utils.plot_model(model, "multi_input_and_output_model.png", show_shapes=True)
    return model


def lstm_train(file_dir, test_dir):
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    count = 0
    save_path_eco = 'LSTM_1.0_model_eco.h5'
    save_path_movement = 'LSTM_1.0_model_movement.h5'
    save_path_dmg = 'LSTM_1.0_model_dmg.h5'
    save_path_flash = 'LSTM_1.0_model_flash.h5'
    save_path_grenade = 'LSTM_1.0_model_grenade.h5'
    save_path_kill = 'LSTM_1.0_model_kill.h5'
    save_path_wf = 'LSTM_1.0_model_weaponfire.h5'
    for item in os.listdir(file_dir):
        if os.path.isdir(os.path.join(file_dir, item)):
            # Only keep the intact data.
            names = good_data_name_list_in_each_folder(os.path.join(file_dir, item))
            for name in names:
                try:
                    # Extract each player's corresponding data
                    economy_df, movement_df, damages_df, flashes_df, grenades_df, kills_df, weapon_fires_df = extract_df(
                        name, os.path.join(file_dir, item))
                    # Preprocess data
                    economy_df_x, economy_df_y = eco_preprocess(economy_df, time_step=3)
                    movement_df_x, movement_df_y = movement_preprocess(movement_df, time_step=512)
                    damages_df_x, damages_df_y = engagement_dmg_preprocess(damages_df, time_step=1)
                    flashes_df_x, flashes_df_y = engagement_flash_preprocess(flashes_df, time_step=1)
                    grenades_df_x, grenades_df_y = engagement_grenade_preprocess(grenades_df, time_step=1)
                    kills_df_x, kills_df_y = engagement_kill_preprocess(kills_df, time_step=1)
                    weapon_fires_df_x, weapon_fires_df_y = engagement_weaponFire_preprocess(weapon_fires_df,
                                                                                            time_step=1)

                    if count == 0:
                        model_eco = construct_eco_model(economy_df_x)
                        model_movement = construct_movement_model(movement_df_x)
                        model_engagement_dmg = construct_engagement_dmg_model(damages_df_x)
                        model_engagement_flash = construct_engagement_flash_model(flashes_df_x)
                        model_engagement_grenade = construct_engagement_grenade_model(grenades_df_x)
                        model_engagement_kill = construct_engagement_kill_model(kills_df_x)
                        model_engagement_weaponFire = construct_engagement_weaponFire_model(weapon_fires_df_x)
                    else:
                        model_eco = keras.models.load_model(save_path_eco)
                        model_movement = keras.models.load_model(save_path_movement)
                        model_engagement_dmg = keras.models.load_model(save_path_dmg)
                        model_engagement_flash = keras.models.load_model(save_path_flash)
                        model_engagement_grenade = keras.models.load_model(save_path_grenade)
                        model_engagement_kill = keras.models.load_model(save_path_kill)
                        model_engagement_weaponFire = keras.models.load_model(save_path_wf)

                    model_eco.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_eco.fit({"Economy Input": economy_df_x}, {"Economy_Prediction": economy_df_y},
                                  epochs=10)
                    model_eco.save(save_path_eco)

                    model_movement.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_movement.fit({"Movement Input": movement_df_x}, {"Movement_Prediction": movement_df_y},
                                       epochs=10)
                    model_movement.save(save_path_movement)

                    model_engagement_dmg.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_engagement_dmg.fit({"Engagement_DMGs Input": damages_df_x},
                                             {"Engagement_DMGs_Prediction": damages_df_y},
                                             epochs=10)
                    model_engagement_dmg.save(save_path_dmg)

                    model_engagement_flash.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_engagement_flash.fit({"Engagement_FLASHES Input": flashes_df_x},
                                               {"Engagement_FLASHES_Prediction": flashes_df_y},
                                               epochs=10)
                    model_engagement_flash.save(save_path_flash)

                    model_engagement_grenade.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_engagement_grenade.fit({"Engagement_GRENADES Input": grenades_df_x},
                                                 {"Engagement_GRENADES_Prediction": grenades_df_y},
                                                 epochs=10)
                    model_engagement_grenade.save(save_path_grenade)

                    model_engagement_kill.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_engagement_kill.fit({"Engagement_KILLS Input": kills_df_x},
                                              {"Engagement_KILLS_Prediction": kills_df_y},
                                              epochs=10)
                    model_engagement_kill.save(save_path_kill)

                    model_engagement_weaponFire.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    model_engagement_weaponFire.fit({"Engagement_WEAPONFIRES Input": weapon_fires_df_x},
                                                    {"Engagement_WEAPONFIRES_Prediction": weapon_fires_df_y},
                                                    epochs=10)
                    model_engagement_weaponFire.save(save_path_wf)

                    # pred1, pred2, pred3, pred4, pred5, pred6, pred7 = model.predict(movement_df_x)
                    # print(pred1, pred2, pred3, pred4, pred5, pred6, pred7)
                    count += 1
                except Exception as ex:
                    with open("LSTM_error_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""LSTM while training: {name} occurs error.""" + "\n")
                        fl.write(f"""Error info: {ex} """ + "\n")


def test_get_all_folder(path):
    # Candidates
    name = []


def lstm_test(test_dir):
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    count = 0
    save_path_eco = 'LSTM_1.0_model_eco.h5'
    save_path_movement = 'LSTM_1.0_model_movement.h5'
    save_path_dmg = 'LSTM_1.0_model_dmg.h5'
    save_path_flash = 'LSTM_1.0_model_flash.h5'
    save_path_grenade = 'LSTM_1.0_model_grenade.h5'
    save_path_kill = 'LSTM_1.0_model_kill.h5'
    save_path_wf = 'LSTM_1.0_model_weaponfire.h5'
    for item in os.listdir(test_dir):
        if os.path.isdir(os.path.join(test_dir, item)):
            # Only keep the intact data.
            names = good_data_name_list_in_each_folder(os.path.join(test_dir, item))
            for name in names:
                try:
                    # Extract each player's corresponding data
                    economy_df, movement_df, damages_df, flashes_df, grenades_df, kills_df, weapon_fires_df = extract_df(
                        name, os.path.join(test_dir, item))
                    # Preprocess data
                    economy_df_x, economy_df_y = eco_preprocess(economy_df, time_step=3)
                    movement_df_x, movement_df_y = movement_preprocess(movement_df, time_step=512)
                    damages_df_x, damages_df_y = engagement_dmg_preprocess(damages_df, time_step=1)
                    flashes_df_x, flashes_df_y = engagement_flash_preprocess(flashes_df, time_step=1)
                    grenades_df_x, grenades_df_y = engagement_grenade_preprocess(grenades_df, time_step=1)
                    kills_df_x, kills_df_y = engagement_kill_preprocess(kills_df, time_step=1)
                    weapon_fires_df_x, weapon_fires_df_y = engagement_weaponFire_preprocess(weapon_fires_df,
                                                                                            time_step=1)

                    model_eco = keras.models.load_model(save_path_eco)
                    model_movement = keras.models.load_model(save_path_movement)
                    model_engagement_dmg = keras.models.load_model(save_path_dmg)
                    model_engagement_flash = keras.models.load_model(save_path_flash)
                    model_engagement_grenade = keras.models.load_model(save_path_grenade)
                    model_engagement_kill = keras.models.load_model(save_path_kill)
                    model_engagement_weaponFire = keras.models.load_model(save_path_wf)

                    model_eco.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    eco_pred = model_eco.predict({"Economy Input": economy_df_x})

                    model_movement.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    movement_pred = model_movement.predict({"Movement Input": movement_df_x})

                    model_engagement_dmg.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    dmg_pred = model_engagement_dmg.predict({"Engagement_DMGs Input": damages_df_x})

                    model_engagement_flash.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    flash_pred = model_engagement_flash.predict({"Engagement_FLASHES Input": flashes_df_x})

                    model_engagement_grenade.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    grenade_pred = model_engagement_grenade.predict({"Engagement_GRENADES Input": grenades_df_x})

                    model_engagement_kill.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    kill_pred = model_engagement_kill.predict({"Engagement_KILLS Input": kills_df_x})

                    model_engagement_weaponFire.compile(
                        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
                        loss='binary_crossentropy',
                        metrics=[keras.metrics.TrueNegatives(), keras.metrics.TruePositives(), "acc"],
                    )
                    wf_pred = model_engagement_weaponFire.predict({"Engagement_WEAPONFIRES Input": weapon_fires_df_x})

                    eco_final_pred = np.mean(eco_pred)
                    movement_final_pred = np.mean(movement_pred)
                    dmg_final_pred = np.mean(dmg_pred)
                    flash_final_pred = np.mean(flash_pred)
                    grenade_final_pred = np.mean(grenade_pred)
                    kill_final_pred = np.mean(kill_pred)
                    wf_final_pred = np.mean(wf_pred)
                    ground_truth = economy_df_y[0]

                    print(eco_final_pred)
                    print(movement_final_pred)
                    print(dmg_final_pred)
                    print(flash_final_pred)
                    print(grenade_final_pred)
                    print(kill_final_pred)
                    print(wf_final_pred)
                    print(ground_truth)

                    with open("LSTM_test.txt", "a", encoding="utf-8") as fl:
                        # write log file
                        fl.write(f"""{name}""" + "\n")
                        fl.write(f"""{eco_final_pred}""" + "\n")
                        fl.write(f"""{movement_final_pred}""" + "\n")
                        fl.write(f"""{dmg_final_pred}""" + "\n")
                        fl.write(f"""{flash_final_pred}""" + "\n")
                        fl.write(f"""{grenade_final_pred}""" + "\n")
                        fl.write(f"""{kill_final_pred}""" + "\n")
                        fl.write(f"""{wf_final_pred}""" + "\n")
                        fl.write(f"""{ground_truth}""" + "\n")
                        fl.write(f"""""" + "\n")

                    count += 1

                except Exception as ex:
                    with open("LSTM_Predict_error_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""LSTM while testing: {name} occurs error.""" + "\n")
                        fl.write(f"""Error info: {ex} """ + "\n")
