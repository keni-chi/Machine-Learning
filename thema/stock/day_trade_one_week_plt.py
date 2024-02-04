import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt

import simulate_conf


# フォルダ作成
SAMPLE_DIR = f'day_trade_{simulate_conf.RUNDATE}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(f'day_trade_{simulate_conf.RUNDATE}')
    os.makedirs(f'day_trade_{simulate_conf.RUNDATE}/one_week')


def one_day_plt():
    df_acc = pd.read_csv(f'simulate_{simulate_conf.RUNDATE}/df_acc.csv', index_col=0, encoding='shift-jis')

    # コード
    code_list = df_acc['コード'].tolist()
    # コード
    data_j = pd.read_csv('data_j_prime.csv', usecols=[0, 1], encoding='shift_jis')
    print(data_j)
    code_list = data_j['コード'].tolist()

    for code in code_list:
        code = str(code)

        try:        
            df_raw = pd.read_csv(f'data-yahoo-day-trade-{simulate_conf.RUNDATE}/stock_'+ str(code) + '.csv', index_col=0, encoding='shift-jis')
        except Exception as e:
            print('except')

        df = df_raw.copy()

        # nanになっている行数をカウント
        nans = df['Open'].isnull().sum()
        if nans / len(df) > 0.2: 
            print('取引が少なくcontinue')
            continue

        df = df.dropna()

        # 前日の終値を取得
        df_one_week = df_raw
        df_one_week = df_one_week.dropna()
        df_one_week_v = df_one_week['Close'].tolist()[-1]
        df = df.reset_index()
        df['Close_ratio'] = df['Close']/df_one_week_v

        # 窓での統計値
        df['mean10'] = df['Close_ratio'].rolling(10).mean()
        df['mean10+0.01'] = df['mean10'] + 0.01
        df['mean10-0.01'] = df['mean10'] - 0.01

        df['mean10_shift1'] = df['mean10'].shift(1)
        df['mean10_diff_raw'] = df['mean10'] - df['mean10_shift1']
        df['mean10_diff_raw_shift1'] = df['mean10_diff_raw'].shift(1)

        df.loc[df['mean10_diff_raw'] > 0, 'flg1'] = 1
        df.loc[df['mean10_diff_raw_shift1'] < 0, 'flg2'] = 1
        df.loc[df['mean10_diff_raw'] > 0.00012, 'flg3'] = 1

        df['mean10_shift2'] = df['mean10'].shift(2)
        df['mean10_diff_raw2'] = df['mean10'] - df['mean10_shift2']
        df.loc[df['mean10_diff_raw2'] > 0, 'flg4'] = 1
        df.loc[df['mean10_diff_raw2'] > 0.00012, 'flg5'] = 1

        df.loc[df['flg1'] + df['flg2'] + df['flg3'] + df['flg4'] + df['flg5'] == 5, 'flgA'] = 1

        df['mean10_diff'] = df['mean10'] - df['mean10_shift1'] + 1

        # 基準値の補助線
        df['1.01'] = 1.01
        df['1.0'] = 1.0
        df['0.99'] = 0.99

        # 描画
        fig, ax = plt.subplots(figsize=(40,4))
        ax.plot(df.index, df['Close_ratio'])
        ax.plot(df.index, df['mean10'])
        ax.plot(df.index, df['mean10+0.01'])
        ax.plot(df.index, df['mean10-0.01'])
        ax.plot(df.index, df['mean10_diff'], label='mean10_diff')
        ax.plot(df.index, df['flgA'], marker='.', label='flgA')
        ax.plot(df.index, df['1.01'], label='1.01')
        ax.plot(df.index, df['1.0'], label='1.0')
        ax.plot(df.index, df['0.99'], label='0.99')
        ax.set_ylim(0.95, 1.05)
        ax.set_xticks([0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600,
                       660, 720, 780, 840, 900, 960, 1020, 1080, 1140, 1200]) 
        # ax.set_yticks([0.9, 1.1])
        # ax.set_yticks([0.9, 0.95, 1.0, 1.05, 1.1]) 
        ax.grid(True)
        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        ax.legend()
        plt.savefig(f'day_trade_{simulate_conf.RUNDATE}/one_week/{code}.png')
        plt.close()

        df.to_csv(f'day_trade_{simulate_conf.RUNDATE}/one_week/{code}.csv')


def main():
    one_day_plt()


if __name__ == '__main__':
    main()