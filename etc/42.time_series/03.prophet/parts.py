import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from fbprophet import Prophet
import warnings
import glob
import os
warnings.filterwarnings('ignore') # 計算警告を非表示


param_number = ''
file_names = []
for f in glob.glob('input_data/*.csv'):
    file_names.append(os.path.split(f)[1])
file_names_target = [s for s in file_names if param_number in s]


# データ読み込み
def read_data():
    years = []
    for i in file_names_target:
        df = pd.read_csv('input_data/' + i, encoding="SHIFT-JIS", header=1)
        years.append(df)
    df_concat = pd.concat(years)
    return df_concat

df = read_data()
df = df[['a', 'b']]
df = df.reset_index(drop=True)
df = df.rename(columns={'a': 'ds'})
df = df.rename(columns={'b': 'y'})
df['ds'] = pd.to_datetime(df['ds'])
df = df.set_index('ds')


# 前処理
new_idx = pd.date_range(df.index[0], df.index[-1], freq='D')
df = df.reindex(new_idx, fill_value=np.nan)
df = df.interpolate()

df_1 = df[:'2000-01-01 00:00']
df_1['y'] = df_1['y'] * 10
df_2 = df['2000-01-21 00:00':]

df = pd.concat([df_1, df_2])
df.head()

plt.plot(df['y'])
plt.show()

df = df.rename_axis('ds').reset_index()

