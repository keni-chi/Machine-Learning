import glob
import pandas as pd
import os
import datetime as dt
path_list = glob.glob('./data/*.csv')


df_dataset = pd.DataFrame()

for path in path_list:
    df = pd.read_csv(path)
    if len(df) == 0:
        continue
    df['Date'] = pd.to_datetime(df['Date'])

    # 日付絞り込み
    df = df[df['Date'] > dt.datetime(2018,1,1)]
    df = df[df['Date'] < dt.datetime(2023,3,1)]

    df = df.set_index('Date')
    df_m = df.resample('M').mean()

    code = path.split('_')[1].split('.')[0]
    print(code)
    print(df_m.head())
    df_m.to_csv( os.path.dirname(__file__) + '/data_month/m_stock_'+ code + '.csv')
    df_dataset[code] = df_m['Close']

df_dataset = df_dataset.T
print(df_dataset)
df_dataset.to_csv( os.path.dirname(__file__) + '/dataset/dataset.csv')
