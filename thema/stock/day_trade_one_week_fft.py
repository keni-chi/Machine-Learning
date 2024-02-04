# https://qiita.com/ks711/items/e472783b3e9baecb5a5a
import pandas as pd
import time
from datetime import timedelta
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

import simulate_conf


# フォルダ作成
SAMPLE_DIR = f'day_trade_{simulate_conf.RUNDATE}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(f'day_trade_{simulate_conf.RUNDATE}')
    os.makedirs(f'day_trade_{simulate_conf.RUNDATE}/one_week')


def bandpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "band")           #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す


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

        # バンドパスをする関数を実行
        # サンプルデータ作成
        n = len(df)                     # データ数
        dt = 0.01                          # サンプリング間隔
        f = 1                           # 周波数
        y = df['Close_ratio']
        yf = np.fft.fft(y)/(n/2)
        freq = np.fft.fftfreq(n, d=dt)
        fs = 10
        yf2 = np.copy(yf)
        yf2[(freq > 100)] = 0
        yf2[(freq < 5)] = 0
        df['fft'] = np.real(np.fft.ifft(yf2)*n) + 1

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
        ax.plot(df.index, df['fft'], label='fft')
        # ax.plot(df.index, df['mean10_diff'], label='mean10_diff')
        # ax.plot(df.index, df['flgA'], marker='.', label='flgA')
        ax.plot(df.index, df['1.01'], label='1.01')
        # ax.plot(df.index, df['1.0'], label='1.0')
        ax.plot(df.index, df['0.99'], label='0.99')
        # ax.set_ylim(0.95, 1.05)
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