import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt
import glob

import simulate_conf


# フォルダ作成
path1 = f'day-trade-{simulate_conf.RUNDATE}'
if not os.path.exists(path1):
    os.makedirs(path1)

path2 = f'day-trade-{simulate_conf.RUNDATE}/diff_min_max'
if not os.path.exists(path2):
    os.makedirs(path2)


def diff_min_max():
    path_list = glob.glob(f'./data-yahoo-{simulate_conf.RUNDATE}/*.csv')
    code_list = []
    high_low_ratio_list = []
    open_close_ratio_list = []

    for path in path_list:
        # code
        code = path.split('_')[1].split('.')[0]
        print(code)

        # データ読み込み
        df_raw = pd.read_csv(path, index_col=0, encoding='shift-jis')
        df = df_raw['2023-12-29': '2023-12-30']

        if len(df)==0:
            continue

        high = df['High'].tolist()[0]
        low = df['Low'].tolist()[0]
        high_low_ratio = high/low

        open = df['Open'].tolist()[0]
        close = df['Close'].tolist()[0]
        open_close_ratio = (close-open)/open

        code_list.append(code)
        high_low_ratio_list.append(high_low_ratio)
        open_close_ratio_list.append(open_close_ratio)

    df_dataset = pd.DataFrame(data={'コード': code_list, 'high_low_ratio': high_low_ratio_list, 'open_close_ratio': open_close_ratio_list})
    df_dataset['コード'] = df_dataset['コード'].astype(int)
    df_acc = pd.read_csv('./data_j_prime.csv', index_col=0, encoding='shift-jis')
    df_dataset = pd.merge(df_dataset, df_acc, on='コード', how='left')
    df_dataset = df_dataset.sort_values(by=['high_low_ratio'])
    df_dataset.to_csv(f'{path2}/df_dataset.csv', encoding='shift_jis')


def main():
    diff_min_max()


if __name__ == '__main__':
    main()