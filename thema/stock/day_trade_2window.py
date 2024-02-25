import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt
import numpy as np

local_rundate = '20240119'


# フォルダ作成
SAMPLE_DIR = f'day_trade_{local_rundate}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(f'day_trade_{local_rundate}')
    os.makedirs(f'day_trade_{local_rundate}/2window')


def one_day_plt():
    # コード
    data_j = pd.read_csv('data_j_prime.csv', encoding='shift_jis')
    data_j = data_j[(data_j['規模区分']=='TOPIX Large70')|(data_j['規模区分']=='TOPIX Mid400')|(data_j['規模区分']=='TOPIX Small 1')]
    print(data_j)
    code_list = data_j['コード'].tolist()
    # code_list = [1852, 1928, 9107, 4502]  #[1803, 1860, 2160, 2168]

    for code in code_list:
        code = str(code)

        try:        
            df_raw = pd.read_csv(f'data-yahoo-day-trade-{local_rundate}/stock_'+ str(code) + '.csv', index_col=0, encoding='shift-jis')
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

        # 移動平均(w=5)
        df['mean5'] = df['Close_ratio'].rolling(5).mean()
        df['mean5_shift1'] = df['mean5'].shift(1)
        df['mean5_coef'] = df['mean5'] - df['mean5_shift1']

        # 買い-----
        # 短期----
        # 移動平均の傾きの平均を求める
        df['mean5_coef_mean'] = df['mean5_coef'].rolling(5).mean()
        # 正であればフラグを立てる
        df.loc[df['mean5_coef_mean'] > 0.0003, 'tempA1'] = 1
        # 追加：移動平均w=20で、現在値がそれより大きな値であれば買い
        df['mean20'] = df['Close_ratio'].rolling(20).mean()
        df.loc[df['Close_ratio'] > df['mean20'], 'tempA2'] = 1
        df.loc[df['tempA1'] + df['tempA2'] == 2, 'up_mean5_coef_mean'] = 1

        # 長期----
        long_term = 60*3  # 30
        # 負であればフラグを立てる
        df.loc[df['mean5_coef'] < 0, 'down_mean5_coef'] = 1
        # 傾き負の数をカウント
        df['down_mean5_coef_count'] = df['down_mean5_coef'].rolling(long_term).count()/long_term
        # 8割以上負であればフラグを立てる
        # df.loc[df['down_mean5_coef_count'] >= 0.55, 'up_down_mean5_coef_count'] = 1
        # ⇒もみ合いのほうが良さそう
        df.loc[df['down_mean5_coef_count'] <= 0.55, 'temp1'] = 1
        df.loc[df['down_mean5_coef_count'] >= 0.5, 'temp2'] = 1
        # 統合
        df.loc[df['temp1'] + df['temp2'] == 2, 'up_down_mean5_coef_count'] = 1
        
        # 長期2----
        df['mean5_shift30'] = df['mean5'].shift(long_term)
        df['shift30_ratio'] = (df['mean5'] - df['mean5_shift30'])/df['mean5']
        # ３０分での下落率がマイナス5%以上であればフラグを立てる
        df.loc[df['shift30_ratio'] >= -0.05, 'down_shift30_ratio'] = 1

        # # peakフラグ列追加
        df.loc[df['up_mean5_coef_mean'] + df['up_down_mean5_coef_count'] + df['down_shift30_ratio'] == 3, 'flg_buy'] = 1
        # フラグ立っている場所の値を埋める
        df["buy_v"] = np.where(df["flg_buy"] == 1, df['mean5'], None)


        # 売り-----
        # 短期----
        # # 移動平均の傾きの平均を求める
        # df['mean5_coef_mean'] = df['mean5_coef'].rolling(5).mean()
        # "正"であればフラグを立てる
        df.loc[df['mean5_coef_mean'] < 0, 'sale_up_mean5_coef_mean'] = 1

        # 長期----
        # "負"であればフラグを立てる
        df.loc[df['mean5_coef'] > 0, 'sale_down_mean5_coef'] = 1
        # 傾き負の数をカウント
        df['sale_down_mean5_coef_count'] = df['sale_down_mean5_coef'].rolling(long_term).count()/long_term
        # 8割以上負であればフラグを立てる
        df.loc[df['sale_down_mean5_coef_count'] >= 0.55, 'sale_up_down_mean5_coef_count'] = 1

        # 長期2----
        # df['mean5_shift30'] = df['mean5'].shift(30)
        # df['shift30_ratio'] = (df['mean5'] - df['mean5_shift30'])/df['mean5']
        # ３０分での下落率が"マイナス5%以上"であればフラグを立てる
        df.loc[df['shift30_ratio'] <= 0.05, 'sale_down_shift30_ratio'] = 1

        # # peakフラグ列追加
        df.loc[df['sale_up_mean5_coef_mean'] + df['sale_up_down_mean5_coef_count'] + df['sale_down_shift30_ratio'] == 3, 'flg_sale'] = 1
        # フラグ立っている場所の値を埋める
        df["sale_v"] = np.where(df["flg_sale"] == 1, df['mean5'], None)

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

        #####
        # 描画
        #####
        fig, ax = plt.subplots(figsize=(40,4))
        ax.plot(df.index, df['Close_ratio'])
        ax.plot(df.index, df['mean5'])
        ax.plot(df.index, df['mean20'])
        ax.plot(df.index, df['buy_v'], marker='.', label='buy_v')
        ax.plot(df.index, df['sale_v'], marker='.', label='sale_v')

        # 縦の補助線
        df_temp = df.copy()
        df_temp = df_temp.dropna(subset=['day_diff_flg'])
        flg_list = df_temp.index.tolist()
        for i in flg_list:
            plt.vlines(i, 0, 2, color='g')

        # グラフ設定
        ax.set_ylim(0.96, 1.04)
        # ax2.set_ylim(0, 2)
        ax.set_xticks([0, 10, 20, 30, 40, 50, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600,
                       660, 720, 780, 840, 900, 960, 1020, 1080, 1140, 1200]) 
        # ax.set_yticks([0.9, 1.1])
        # ax.set_yticks([0.9, 0.95, 1.0, 1.05, 1.1]) 
        ax.grid(True)
        # ax.set_xlabel('x')
        # ax.set_ylabel('y')
        ax.legend()
        plt.savefig(f'day_trade_{local_rundate}/2window/{code}.png')
        plt.close()

        df.to_csv(f'day_trade_{local_rundate}/2window/{code}.csv')


def main():
    one_day_plt()


if __name__ == '__main__':
    main()