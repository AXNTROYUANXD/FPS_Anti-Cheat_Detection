import pandas as pd
import os
import shutil
import numpy as np


def playerFrame_file_process(root, df, cheater):
    grouped = df.groupby(['tick', 'side'])
    center_coords = grouped[['x', 'y', 'z']].transform(np.mean)
    center_coords = center_coords.reindex(df.index).values.tolist()

    isolation_degrees = np.linalg.norm(df[['x', 'y', 'z']].values - center_coords, axis=1)

    df['IsolationDegree'] = isolation_degrees

    # Add 'isCheater' column
    df["isCheater"] = (df["name"] == cheater).astype(int)

    try:
        # Drop the tuples where 'isBot' is 'TRUE'
        df = df.drop(df[df['isBot'] == 'TRUE'].index)
    except:
        pass

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['side'].notna(), 'side'] = df.loc[df['side'].notna(), 'side'].replace(
        {'CT': 1, 'T': 2})

    # Drop the tuples where 'isUnknown' is 'TRUE'
    df = df.drop(df[df['isUnknown'] == 'TRUE'].index)

    # Convert True/False to 1/0
    bool_columns = ["isAlive", "isBlinded", "isAirborne", "isDucking", "isDuckingInProgress",
                    "isUnDuckingInProgress", "isDefusing", "isPlanting", "isReloading", "isInBombZone", "isInBuyZone",
                    "isStanding", "isScoped", "isWalking", "isUnknown"]
    df[bool_columns] = df[bool_columns].astype(int)

    columns_to_drop = ["isBot", "teamName", "team", "eyeX", "eyeY", "eyeZ", "hp", "armor", "activeWeapon",
                       "flashGrenades", "smokeGrenades",
                       "heGrenades", "fireGrenades", "totalUtility", "lastPlaceName",
                       "isInBuyZone", "isUnknown", "spotters", "equipmentValue", "equipmentValueFreezetimeEnd",
                       "equipmentValueRoundStart", "cash", "cashSpendThisRound", "cashSpendTotal", "hasHelmet",
                       "hasDefuse",
                       "hasBomb", "ping", "zoomLevel", "matchID", "mapName"]
    try:
        df = df.drop(columns_to_drop, axis=1, errors='raise')
    except KeyError:
        pass

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    # ATKer names
    names = df["name"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_playerFrames_Processed.csv"
        df_new = df[df["name"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_playerFrames_Processed.csv"
        filename_new = f"{name}_playerFrames_Processed.csv"
        foldername = f"{name}_Movement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def movement_preprocess(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            # Process playerFrames.csv file
            if '_playerFrames.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0, low_memory=False)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    playerFrame_file_process(root, df, cheater)
                except:
                    with open("playerFrames_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

