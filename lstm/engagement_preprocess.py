import pandas as pd
import os
import shutil


def kill_file_process(root, df, cheater):
    # Add 'isCheater' column
    df["isCheater"] = (df["attackerName"] == cheater).astype(int)

    # Drop the tuples where 'attackerName' is null
    df.dropna(subset=['attackerName'], inplace=True)
    # Drop the tuples where 'weapons' is 'C4'
    df = df.drop(df[df['weapon'] == 'C4'].index)
    # Drop the tuples where 'weapons' is 'World'
    df = df.drop(df[df['weapon'] == 'World'].index)

    # Convert True/False to 1/0
    bool_columns = ["isSuicide", "isTeamkill", "isWallbang", "isFirstKill", "isHeadshot", "victimBlinded",
                    "attackerBlinded", "noScope", "thruSmoke", "isTrade"]
    df[bool_columns] = df[bool_columns].astype(int)

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['attackerSide'].notna(), 'attackerSide'] = df.loc[df['attackerSide'].notna(), 'attackerSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['victimSide'].notna(), 'victimSide'] = df.loc[df['victimSide'].notna(), 'victimSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['assisterSide'].notna(), 'assisterSide'] = df.loc[df['assisterSide'].notna(), 'assisterSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['flashThrowerSide'].notna(), 'flashThrowerSide'] = df.loc[
        df['flashThrowerSide'].notna(), 'flashThrowerSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['playerTradedSide'].notna(), 'playerTradedSide'] = df.loc[
        df['playerTradedSide'].notna(), 'playerTradedSide'].replace(
        {'CT': 1, 'T': 2})

    df.loc[df['weapon'].notna(), 'weapon'] = df.loc[
        df['weapon'].notna(), 'weapon'].replace({
                'AWP': 100,
        'G3SG1': 101,
        'SCAR-20': 102,
        'SSG 08': 103,
        'AK-47': 200,
        'AUG': 201,
        'FAMAS': 202,
        'Galil AR': 203,
        'M4A1-S': 204,
        'M4A4': 205,
        'SG 553': 206,
        'M4A1': 207,
        'MAC-10': 300,
        'MP5-SD': 301,
        'MP7': 302,
        'MP9': 303,
        'P90': 304,
        'PP-Bizon': 305,
        'UMP-45': 306,
        'M249': 400,
        'Negev': 401,
        'MAG-7': 500,
        'Nova': 501,
        'Sawed-Off': 502,
        'XM1014': 503,
        'CZ75-Auto': 600,
        'Desert Eagle': 601,
        'Dual Berettas': 602,
        'Five-SeveN': 603,
        'Glock-18': 604,
        'P2000': 605,
        'P250': 606,
        'R8 Revolver': 607,
        'Tec-9': 608,
        'USP-S': 609,
        'USP': 610,
        'CZ75 Auto': 611,
        'HE Grenade': 700,
        'Molotov': 701,
        'Smoke Grenade': 702,
        'Flashbang': 703,
        'Decoy Grenade': 704,
        'Incendiary Grenade': 705,
        'Knife': 800,
        'Zeus x27': 801
    })
    df.loc[df['weaponClass'].notna(), 'weaponClass'] = df.loc[
        df['weaponClass'].notna(), 'weaponClass'].replace({
        'Rifle': 100,
        'SMG': 300,
        'Heavy': 400,
        'Pistols': 600,
        'Grenade': 700,
        'Equipment': 800
    })

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    df = df.drop(
        ["clockTime", "attackerTeam", "victimName", "victimTeam", "playerTradedName", "playerTradedTeam", "matchID",
         "mapName", "assisterName"], axis=1)

    # ATKer names
    names = df["attackerName"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_Kills_Processed.csv"
        df_new = df[df["attackerName"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_Kills_Processed.csv"
        filename_new = f"{name}_Kills_Processed.csv"
        foldername = f"{name}_Engagement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def fire_file_process(root, df, cheater):
    # Add 'isCheater' column
    df["isCheater"] = (df["playerName"] == cheater).astype(int)

    # Convert True/False to 1/0
    bool_columns = ["playerStrafe"]
    df[bool_columns] = df[bool_columns].astype(int)

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['playerSide'].notna(), 'playerSide'] = df.loc[df['playerSide'].notna(), 'playerSide'].replace(
        {'CT': 1, 'T': 2})

    df.loc[df['weapon'].notna(), 'weapon'] = df.loc[
        df['weapon'].notna(), 'weapon'].replace({
        'AWP': 100,
        'G3SG1': 101,
        'SCAR-20': 102,
        'SSG 08': 103,
        'AK-47': 200,
        'AUG': 201,
        'FAMAS': 202,
        'Galil AR': 203,
        'M4A1-S': 204,
        'M4A4': 205,
        'SG 553': 206,
        'M4A1': 207,
        'MAC-10': 300,
        'MP5-SD': 301,
        'MP7': 302,
        'MP9': 303,
        'P90': 304,
        'PP-Bizon': 305,
        'UMP-45': 306,
        'M249': 400,
        'Negev': 401,
        'MAG-7': 500,
        'Nova': 501,
        'Sawed-Off': 502,
        'XM1014': 503,
        'CZ75-Auto': 600,
        'Desert Eagle': 601,
        'Dual Berettas': 602,
        'Five-SeveN': 603,
        'Glock-18': 604,
        'P2000': 605,
        'P250': 606,
        'R8 Revolver': 607,
        'Tec-9': 608,
        'USP-S': 609,
        'USP': 610,
        'CZ75 Auto': 611,
        'HE Grenade': 700,
        'Molotov': 701,
        'Smoke Grenade': 702,
        'Flashbang': 703,
        'Decoy Grenade': 704,
        'Incendiary Grenade': 705,
        'Knife': 800,
        'Zeus x27': 801
    })
    df.loc[df['weaponClass'].notna(), 'weaponClass'] = df.loc[
        df['weaponClass'].notna(), 'weaponClass'].replace({
        'Rifle': 100,
        'SMG': 300,
        'Heavy': 400,
        'Pistols': 600,
        'Grenade': 700,
        'Equipment': 800
    })

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    df = df.drop(
        ["clockTime", "playerTeam", "matchID", "mapName"], axis=1)

    # ATKer names
    names = df["playerName"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_weaponFires_Processed.csv"
        df_new = df[df["playerName"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_weaponFires_Processed.csv"
        filename_new = f"{name}_weaponFires_Processed.csv"
        foldername = f"{name}_Engagement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def damage_file_process(root, df, cheater):
    # Add 'isCheater' column
    df["isCheater"] = (df["attackerName"] == cheater).astype(int)

    # Drop the tuples where 'attackerName' is null
    df.dropna(subset=['attackerName'], inplace=True)
    # Drop the tuples where 'weapons' is 'C4'
    df = df.drop(df[df['weapon'] == 'C4'].index)
    # Drop the tuples where 'weapons' is 'World'
    df = df.drop(df[df['weapon'] == 'World'].index)

    # Convert True/False to 1/0
    bool_columns = ["isFriendlyFire", "attackerStrafe"]
    df[bool_columns] = df[bool_columns].astype(int)

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['attackerSide'].notna(), 'attackerSide'] = df.loc[df['attackerSide'].notna(), 'attackerSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['victimSide'].notna(), 'victimSide'] = df.loc[df['victimSide'].notna(), 'victimSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['hitGroup'].notna(), 'hitGroup'] = df.loc[df['hitGroup'].notna(), 'hitGroup'].replace(
        {'Generic': 0,
         'Head': 1,
         'Chest': 2,
         'Stomach': 3,
         'LeftArm': 4,
         'RightArm': 5,
         'LeftLeg': 6,
         'RightLeg': 7,
         'Neck': 8
         })

    df.loc[df['weapon'].notna(), 'weapon'] = df.loc[
        df['weapon'].notna(), 'weapon'].replace({
        'AWP': 100,
        'G3SG1': 101,
        'SCAR-20': 102,
        'SSG 08': 103,
        'AK-47': 200,
        'AUG': 201,
        'FAMAS': 202,
        'Galil AR': 203,
        'M4A1-S': 204,
        'M4A4': 205,
        'SG 553': 206,
        'M4A1': 207,
        'MAC-10': 300,
        'MP5-SD': 301,
        'MP7': 302,
        'MP9': 303,
        'P90': 304,
        'PP-Bizon': 305,
        'UMP-45': 306,
        'M249': 400,
        'Negev': 401,
        'MAG-7': 500,
        'Nova': 501,
        'Sawed-Off': 502,
        'XM1014': 503,
        'CZ75-Auto': 600,
        'Desert Eagle': 601,
        'Dual Berettas': 602,
        'Five-SeveN': 603,
        'Glock-18': 604,
        'P2000': 605,
        'P250': 606,
        'R8 Revolver': 607,
        'Tec-9': 608,
        'USP-S': 609,
        'USP': 610,
        'CZ75 Auto': 611,
        'HE Grenade': 700,
        'Molotov': 701,
        'Smoke Grenade': 702,
        'Flashbang': 703,
        'Decoy Grenade': 704,
        'Incendiary Grenade': 705,
        'Knife': 800,
        'Zeus x27': 801
    })
    df.loc[df['weaponClass'].notna(), 'weaponClass'] = df.loc[
        df['weaponClass'].notna(), 'weaponClass'].replace({
        'Rifle': 100,
        'SMG': 300,
        'Heavy': 400,
        'Pistols': 600,
        'Grenade': 700,
        'Equipment': 800
    })

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    df = df.drop(
        ["clockTime", "attackerTeam", "victimName", "victimTeam", "matchID", "mapName"], axis=1)

    # ATKer names
    names = df["attackerName"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_damages_Processed.csv"
        df_new = df[df["attackerName"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_damages_Processed.csv"
        filename_new = f"{name}_damages_Processed.csv"
        foldername = f"{name}_Engagement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def grenade_file_process(root, df, cheater):
    # Add 'isCheater' column
    df["isCheater"] = (df["throwerName"] == cheater).astype(int)

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['throwerSide'].notna(), 'throwerSide'] = df.loc[df['throwerSide'].notna(), 'throwerSide'].replace(
        {'CT': 1, 'T': 2})

    df.loc[df['grenadeType'].notna(), 'grenadeType'] = df.loc[
        df['grenadeType'].notna(), 'grenadeType'].replace({
                'AWP': 100,
        'G3SG1': 101,
        'SCAR-20': 102,
        'SSG 08': 103,
        'AK-47': 200,
        'AUG': 201,
        'FAMAS': 202,
        'Galil AR': 203,
        'M4A1-S': 204,
        'M4A4': 205,
        'SG 553': 206,
        'M4A1': 207,
        'MAC-10': 300,
        'MP5-SD': 301,
        'MP7': 302,
        'MP9': 303,
        'P90': 304,
        'PP-Bizon': 305,
        'UMP-45': 306,
        'M249': 400,
        'Negev': 401,
        'MAG-7': 500,
        'Nova': 501,
        'Sawed-Off': 502,
        'XM1014': 503,
        'CZ75-Auto': 600,
        'Desert Eagle': 601,
        'Dual Berettas': 602,
        'Five-SeveN': 603,
        'Glock-18': 604,
        'P2000': 605,
        'P250': 606,
        'R8 Revolver': 607,
        'Tec-9': 608,
        'USP-S': 609,
        'USP': 610,
        'HE Grenade': 700,
        'Molotov': 701,
        'Smoke Grenade': 702,
        'Flashbang': 703,
        'Decoy Grenade': 704,
        'Incendiary Grenade': 705,
        'Knife': 800,
        'Zeus x27': 801
    })

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    df = df.drop(
        ["throwClockTime", "destroyClockTime", "throwerTeam", "entityId", "matchID", "mapName"], axis=1)

    # ATKer names
    names = df["throwerName"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_grenades_Processed.csv"
        df_new = df[df["throwerName"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_grenades_Processed.csv"
        filename_new = f"{name}_grenades_Processed.csv"
        foldername = f"{name}_Engagement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def flash_file_process(root, df, cheater):
    # Add 'isCheater' column
    df["isCheater"] = (df["attackerName"] == cheater).astype(int)

    # Convert side to CT:1, T:2, omit NaN tuples.
    df.loc[df['attackerSide'].notna(), 'attackerSide'] = df.loc[df['attackerSide'].notna(), 'attackerSide'].replace(
        {'CT': 1, 'T': 2})
    df.loc[df['playerSide'].notna(), 'playerSide'] = df.loc[df['playerSide'].notna(), 'playerSide'].replace(
        {'CT': 1, 'T': 2})

    # replace all nulls as zeros
    df.fillna(0, inplace=True)

    df = df.drop(
        ["clockTime", "attackerTeam", "playerName", "playerTeam", "matchId", "mapName"], axis=1)

    # ATKer names
    names = df["attackerName"].unique()
    # Create new CSVs
    for name in names:
        filename_new = f"{name}_flashes_Processed.csv"
        df_new = df[df["attackerName"] == name]

        df_new.to_csv(os.path.join(root, filename_new), index=False)

        filename_old = f"{name}_flashes_Processed.csv"
        filename_new = f"{name}_flashes_Processed.csv"
        foldername = f"{name}_Engagement"

        # Create folder if not exist
        if not os.path.exists(os.path.join(root, foldername)):
            os.makedirs(os.path.join(root, foldername))
            # print(f"Folder '{foldername}' created.")

        # Move file
        shutil.move(os.path.join(root, filename_old), os.path.join(root, foldername, filename_new))
        # print(f"File '{filename_new}' moved to folder '{foldername}'.")


def engagement_integrity_check(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if '_Engagement' in dirpath:
            tempName = os.path.basename(dirpath).split('_Engagement')[0]

            grenade_file = os.path.join(dirpath, tempName + '_grenades_Processed.csv')

            if not os.path.exists(grenade_file):
                columns = ['throwTick', 'destroyTick', 'throwSeconds', 'destroySeconds', 'throwerSteamID',
                           'throwerName', 'throwerSide', 'throwerX', 'throwerY', 'throwerZ', 'grenadeType',
                           'grenadeX', 'grenadeY', 'grenadeZ', 'roundNum', 'isCheater']
                df = pd.DataFrame(columns=columns)
                df.to_csv(grenade_file, index=False)
                try:
                    weapon_file = os.path.join(dirpath, tempName + '_weaponFires_Processed.csv')
                    df_weapon = pd.read_csv(weapon_file, nrows=1)
                    playerSteamID = df_weapon['playerSteamID'][0]
                    playerName = df_weapon['playerName'][0]
                    isCheater = df_weapon['isCheater'][0]

                    df = pd.read_csv(grenade_file)
                    row = [0] * len(columns)
                    row[columns.index('throwerSteamID')] = playerSteamID
                    row[columns.index('throwerName')] = playerName
                    row[columns.index('isCheater')] = isCheater
                    df.loc[len(df)] = row
                    df.to_csv(grenade_file, index=False)
                except:
                    with open("integrity_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {dirpath} occurs error.""" + "\n")

            flash_file = os.path.join(dirpath, tempName + '_flashes_Processed.csv')

            if not os.path.exists(flash_file):
                columns = ['tick', 'seconds', 'attackerSteamID', 'attackerName', 'attackerSide', 'attackerX',
                           'attackerY', 'attackerZ', 'attackerViewX', 'attackerViewY', 'playerSteamID', 'playerSide',
                           'playerX', 'playerY', 'playerZ', 'playerViewX', 'playerViewY', 'flashDuration', 'roundNum',
                           'isCheater']
                df = pd.DataFrame(columns=columns)
                df.to_csv(flash_file, index=False)
                try:
                    weapon_file = os.path.join(dirpath, tempName + '_weaponFires_Processed.csv')
                    df_weapon = pd.read_csv(weapon_file, nrows=1)
                    playerSteamID = df_weapon['playerSteamID'][0]
                    playerName = df_weapon['playerName'][0]
                    isCheater = df_weapon['isCheater'][0]

                    df = pd.read_csv(flash_file)
                    row = [0] * len(columns)
                    row[columns.index('attackerSteamID')] = playerSteamID
                    row[columns.index('attackerName')] = playerName
                    row[columns.index('isCheater')] = isCheater
                    df.loc[len(df)] = row
                    df.to_csv(flash_file, index=False)
                except:
                    with open("integrity_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {dirpath} occurs error.""" + "\n")


def engagement_preprocess(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            # Process kills.csv file
            if '_kills.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    kill_file_process(root, df, cheater)
                except:
                    with open("kills_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

            # Process weaponFires.csv file
            if '_weaponFires.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    fire_file_process(root, df, cheater)
                except:
                    with open("weaponFires_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

            # Process damages.csv file
            if '_damages.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    damage_file_process(root, df, cheater)
                except:
                    with open("damages_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

            # Process grenades.csv file
            if '_grenades.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    grenade_file_process(root, df, cheater)
                except:
                    with open("grenades_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

            # Process flashes.csv file
            if '_flashes.csv' in f:
                try:
                    df = pd.read_csv(os.path.join(root, f), index_col=0)
                    # If processing the cheater files, otherwise omit this line and 'isCheater' all mark as 0
                    cheater = f.split("_")[0]
                    flash_file_process(root, df, cheater)
                except:
                    with open("flashes_log.txt", "a") as fl:
                        # write log file
                        fl.write(f"""File: {f} occurs error.""" + "\n")

        # Engagement folder integrity check
        engagement_integrity_check(root)
