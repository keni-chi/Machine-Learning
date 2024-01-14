import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt

import simulate_conf


# フォルダ作成
SAMPLE_DIR = f'day-trade-{simulate_conf.RUNDATE}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(SAMPLE_DIR)
    os.makedirs(SAMPLE_DIR + '/png')


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
        df_raw = pd.read_csv(f'data-yahoo-day-trade-{simulate_conf.RUNDATE}/stock_'+ str(code) + '.csv', index_col=0, encoding='shift-jis')
        df = df_raw['2023-12-29':]

        # nanになっている行数をカウント
        nans = df['Open'].isnull().sum()
        if nans / len(df) > 0.5: 
            print('取引が少なくcontinue')
            continue
        df = df.dropna()
        # print(df)

        # 前日の終値を取得
        df_yesterday = df_raw['2023-12-28':'2023-12-29']
        df_yesterday = df_yesterday.dropna()
        yesterday_close_v = df_yesterday['Close'].tolist()[-1]
        print(df_yesterday)
        print(yesterday_close_v)
        df = df.reset_index()
        df['Close_ratio'] = df['Close']/yesterday_close_v

        # 基準値の補助線
        df['1.0'] = 1.0
        df['0.99'] = 0.99

        # 描画
        fig, ax = plt.subplots(figsize=(16,4))
        ax.plot(df.index, df['Close_ratio'])
        ax.plot(df.index, df['1.0'], label='1.0')
        ax.plot(df.index, df['0.99'], label='0.99')
        ax.set_ylim(0.95, 1.05)
        ax.set_xticks([0, 60, 120, 180, 240, 300]) 
        # ax.set_yticks([0.9, 1.1])
        # ax.set_yticks([0.9, 0.95, 1.0, 1.05, 1.1]) 
        ax.grid(True)
        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        ax.legend()
        plt.savefig(f'{SAMPLE_DIR}/png/oneday_{code}.png')
        plt.close()



def main():
    one_day_plt()


if __name__ == '__main__':
    main()