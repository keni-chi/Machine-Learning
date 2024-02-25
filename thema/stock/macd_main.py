import os
import pandas as pd
import time
import glob
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt


local_rundate = '20240119'

#codeリスト
df_code = pd.read_csv(f'./day_trade_code.csv', index_col=0, encoding='shift-jis')
code_list = df_code['コード'].tolist()


for code in code_list[0:3]:
    print('---------')
    print(code)
    code = str(code)

    # 生データ読み込み
    # df = pd.read_csv(f'./data-yahoo-{local_rundate}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')
    df = pd.read_csv(f'./data-yahoo-day-trade-{local_rundate}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis', parse_dates=True)
    print(df)

    # 欠損処理、インデックス処理
    df = df.dropna(subset='Close')
    df = df.reset_index().reset_index(drop=True)

    # 移動平均
    df['mean25'] = df['Close'].rolling(25).mean()
    df['mean75'] = df['Close'].rolling(75).mean()

    # MACD計算
    exp12 = df['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26

    # シグナル計算
    df['Signal'] = df['MACD'].rolling(window=9).mean()

    # ヒストグラム(MACD - シグナル)
    df['Hist'] = df['MACD'] - df['Signal']

    # diffが正,負の場合のフラグを立てる
    df['flg_seifu'] = 0
    df.loc[df['Hist'] > 0, 'flg_seifu'] = 1
    df['diff'] = df['flg_seifu'] - df['flg_seifu'].shift(1)
    print(df)

    # 買い：macdがsignalを上回った時(diff=1)
    df["kai_v"] = np.where(df["diff"] == 1, df['Close'], None)
    kai_list = df["kai_v"].dropna().tolist()[:-1]
    print(len(kai_list))
    print(kai_list)
    # 売り
    df["uri_v"] = np.where(df["diff"] == -1, df['Close'], None)
    uri_list = df["uri_v"].dropna().tolist()
    print(len(uri_list))
    print(uri_list)
    # 売買
    urikai_list = [x - y for (x, y) in zip(kai_list, uri_list)]
    sum_urikai = sum(urikai_list)
    print(sum_urikai)

    df.to_csv(f'macd/{local_rundate}/{code}.csv', encoding='shift-jis')

    #####
    # 描画
    #####
    # print(len(df))
    # print(df)
    fig, ax = plt.subplots(figsize=(40,4))
    ax.plot(df.index, df['Close'])
    ax.plot(df.index, df['mean25'])
    ax.plot(df.index, df['mean75'])
    ax.plot(df.index, df['kai_v'], marker='.', label='kai_v')
    ax.plot(df.index, df['uri_v'], marker='.', label='uri_v')
    ax.legend()
    # plt.show()
    # plt.close()


    # # MACDとシグナルのプロット作成
    # add_plot = [mpf.make_addplot(df['MACD'], color='m', panel=1, secondary_y=False),
    #     mpf.make_addplot(df['Signal'], color='c', panel=1, secondary_y=False),
    #     mpf.make_addplot(df['Hist'], type='bar', color='g', panel=1, secondary_y=True)]

    # # チャート表示
    # mpf.plot(df, figsize=(32,16), type='candle', mav=(5, 25, 75), volume=True, addplot=add_plot, volume_panel=2, savefig=f'macd/{local_rundate}/{code}.png')
    # # mpf.plot(df, figsize=(32,16), title=code, type='candle', mav=(5, 25), volume=True, addplot=add_plot, volume_panel=2, savefig=f'macd/{local_rundate}/{code}.png')
