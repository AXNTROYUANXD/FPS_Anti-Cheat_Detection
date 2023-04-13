import pandas as pd

df = pd.read_csv('LSTM_test.txt', sep='\n\n', header=None, encoding='utf-8')

print(df)

data = []
for i in range(831):
    # row0 = df.iloc[9 * i, 0].split('\n')[0]
    row1 = df.iloc[9 * i + 1, 0].split('\n')[0]
    row2 = df.iloc[9 * i + 2, 0].split('\n')[0]
    row3 = df.iloc[9 * i + 3, 0].split('\n')[0]
    row4 = df.iloc[9 * i + 4, 0].split('\n')[0]
    row5 = df.iloc[9 * i + 5, 0].split('\n')[0]
    row6 = df.iloc[9 * i + 6, 0].split('\n')[0]
    row7 = df.iloc[9 * i + 7, 0].split('\n')[0]
    row8 = df.iloc[9 * i + 8, 0].split('\n')[0]
    data.append([
        # str(row0),
        float(row1),
        float(row2),
        float(row3),
        float(row4),
        float(row5),
        float(row6),
        float(row7),
        int(row8)
    ])

df_new = pd.DataFrame(data, columns=[
    # 'ID',
    'eco_final_pred',
    'movement_final_pred',
    'dmg_final_pred',
    'flash_final_pred',
    'grenade_final_pred',
    'kill_final_pred',
    'wf_final_pred',
    'ground_truth'
])
df_new.to_csv('LSTM_test.csv', index=False)
