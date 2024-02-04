import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt
import numpy as np

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
    # code_list = [1852, 1928, 9107, 4502]  #[1803, 1860, 2160, 2168]

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
        w = 5
        df['mean' + str(w)] = df['Close_ratio'].rolling(w).mean()

        ####
        #購入
        ####
        # diff
        df['mean' + str(w) + '_s1'] = df['mean' + str(w)].shift(1)
        df['mean' + str(w) + '_diff0'] = df['mean' + str(w)] - df['mean' + str(w) + '_s1']
        df['mean' + str(w) + '_diff1'] = df['mean' + str(w) + '_diff0'].shift(1)

        # peak
        df.loc[df['mean' + str(w) + '_diff0'] > 0, 'flg1'] = 1
        df.loc[df['mean' + str(w) + '_diff1'] < 0, 'flg2'] = 1

        # peakフラグ列追加
        df.loc[df['flg1'] + df['flg2']== 2, 'flgA'] = 1

        # フラグ立っている場所の値を埋める
        df["flg_mean_v"] = np.where(df["flgA"] == 1, df['mean' + str(w)], None)
        # df["flg_Close_ratio_v"] = np.where(df["flgA"] == 1, df['Close_ratio'], None)

        #####
        # 10分前などの点で傾きが正となるものに絞り込み
        #####
        df['mean' + str(w) + '_s5'] = df['mean' + str(w)].shift(5)
        df['mean' + str(w) + '_s10'] = df['mean' + str(w)].shift(10)
        df['mean' + str(w) + '_s60'] = df['mean' + str(w)].shift(60)
        df['mean' + str(w) + '_diff5'] = df['mean' + str(w)] - df['mean' + str(w) + '_s5']
        df['mean' + str(w) + '_diff10'] = df['mean' + str(w)] - df['mean' + str(w) + '_s10']
        df['mean' + str(w) + '_diff60'] = df['mean' + str(w)] - df['mean' + str(w) + '_s60']
        # 正であればフラグを立てる
        df.loc[df['mean' + str(w) + '_diff5'] > 0, 'flg5'] = 1
        df.loc[df['mean' + str(w) + '_diff10'] > 0, 'flg10'] = 1
        df.loc[df['mean' + str(w) + '_diff60'] > 0, 'flg60'] = 1
        # peakフラグ列追加
        df.loc[df['flgA'] + df['flg5'] + df['flg10'] + df['flg60']== 4, 'flgA10'] = 1
        # フラグ立っている場所の値を埋める
        df["flgA10_mean_v"] = np.where(df["flgA10"] == 1, df['mean' + str(w)], None)

        #####
        # 最初のみエントリー（前のピーク検出の時の値より値が大きければ対象外とする）
        #####
        print(df)
        df_first = df.copy()
        df_first = df_first.dropna(subset=['flgA10_mean_v'])
        # df_first = df_first[df_first['flgA10_mean_v'] != None]
        # print('df_first')
        # print(df_first)
        df_first['f_flgA10_mean_v'] = df_first['flgA10_mean_v'].shift(1)
        df_first['f_diff'] = df_first['flgA10_mean_v'] - df_first['f_flgA10_mean_v']
        # df_first.to_csv('test.csv')
        # diffが負の場合のみフラグを立てる
        df_first.loc[df_first['f_diff'] < 0, 'f_flg'] = 1
        # フラグ立っている場所の値を埋める
        df_first["f_v"] = np.where(df_first["f_flg"] == 1, df_first['mean' + str(w)], None)
        df_first = df_first[['f_v']]
        # フラグをもとのdfへマージ    df_ab_i.join(df_ac_i, how='left')
        df = df.join(df_first, how='left')

        ####
        #日付の変わり目の検出
        ####
        df = pd.concat([df, df['timestamp'].str.split('-', expand=True)], axis=1)
        df = df.drop([0, 1], axis=1)
        df = pd.concat([df, df[2].str.split(' ', expand=True)], axis=1)
        df = df.drop([1, 2], axis=1)
        df = df.rename(columns={0: 'day'})
        df['day'] = df['day'].astype(int)
        df['day_diff'] = df['day'] - df['day'].shift(1)
        # フラグを立てる
        df['day_diff_flg'] = np.where(df["day_diff"] == 1, 1, None)
        print('日付の変わり目の検出')
        print(df)

        ####
        #出来高
        ####
        volume_mean = df['Volume'].mean()
        df['Volume_ratio'] = df['Volume'].rolling(10).mean()/volume_mean

        #####
        # 描画
        #####
        fig, ax = plt.subplots(figsize=(40,4))
        ax.plot(df.index, df['Close_ratio'])
        ax.plot(df.index, df['mean' + str(w)])
        ax2 = ax.twinx()

        # 購入検出値
        # ax.plot(df.index, df['flg_mean_v'], marker='.', label='flg_mean_v')
        # ax.plot(df.index, df['flgA10_mean_v'], marker='.', label='flgA10_mean_v')
        ax.plot(df.index, df['f_v'], marker='.', label='f_v')
        ax2.plot(df.index, df['Volume_ratio'], marker='.', label='Volume_ratio')

        # 縦の補助線
        df_temp = df.copy()
        df_temp = df_temp.dropna(subset=['day_diff_flg'])
        flg_list = df_temp.index.tolist()
        for i in flg_list:
            plt.vlines(i, 0, 2, color='g')

        # グラフ設定
        # ax.set_ylim(0.95, 1.05)
        ax2.set_ylim(0, 2)
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600,
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