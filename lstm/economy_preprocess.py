import os
import shutil

import pandas as pd


def eco_file_process(root, df, cheater):
    df_last = df.groupby(['roundNum']).tail(1)
    df = df[
        df.apply(lambda x: (x['roundNum'], x['tick']) in zip(df_last['roundNum'], df_last['tick']), axis=1)]

    try:
        # Drop the tuples where 'isBot' is 'TRUE'
        df = df.drop(df[df['isBot'] == 'TRUE'].index)
    except:
        pass

    # Drop the tuples where 'isUnknown' is 'TRUE'
    df = df.drop(df[df['isUnknown'] == 'TRUE'].index)

    columns_to_drop = ['seconds', 'side', 'teamName', 'team', 'x', 'y', 'z', 'eyeX', 'eyeY', 'eyeZ', 'velocityX',
                       'velocityY', 'velocityZ', 'viewX', 'viewY', 'hp', 'armor', 'activeWeapon', 'flashGrenades',
                       'smokeGrenades', 'heGrenades', 'fireGrenades', 'totalUtility', 'lastPlaceName', 'isAlive',
                       'isBot', 'isBlinded', 'isAirborne', 'isDucking', 'isDuckingInProgress', 'isUnDuckingInProgress',
                       'isDefusing', 'isPlanting', 'isReloading', 'isInBombZone', 'isInBuyZone', 'isStanding',
                       'isScoped', 'isWalking', 'isUnknown', 'spotters', 'equipmentValue', 'ping', 'zoomLevel',
                       'matchID', 'mapName', 'cashSpendThisRound']

    # Add 'isCheater' column
    df["isCheater"] = (df["name"] == cheater).astype(int)

    try:
        df = df.drop(columns_to_drop, axis=1, errors='raise')
    except KeyError:
        pass

    # Convert True/False to 1/0
    bool_columns = ["hasHelmet", "hasDefuse", "hasBomb"]
    df[bool_columns] = df[bool_columns].astype(int)

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    # ATKer names
    names = df["name"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_eco_Processed.csv"
        df_new = df[df["name"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_eco_Processed.csv"
        filename_new = f"{name}_eco_Processed.csv"
        foldername = f"{name}_Economy"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def economy_preprocess(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            # Process playerFrames.csv file
            if '_playerFrames.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0, low_memory=False)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    eco_file_process(root, df, cheater)
                except:
                    with open("eco_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")
