import pandas as pd


def main(data_path):
    df_nade_data = pd.read_csv(f'{data_path}/Final.csv')
    df_angle_data = pd.read_csv('./data_to_combine/angle_fin_data.csv')
    df_hit_data = pd.read_csv('./data_to_combine/hit_fin_data.csv')

    # TODO: combine aim to kill data
    df = pd.merge(df_nade_data, df_angle_data, how='inner', on='ID')
    df = pd.merge(df, df_hit_data, how='inner', on='ID')

    df.to_csv('../classification_all_feature_data_trained.csv')
