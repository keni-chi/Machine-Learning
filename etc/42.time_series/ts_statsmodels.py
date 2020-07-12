import statsmodels.api as sm
import pandas as pd
import numpy as np
import requests
import io
from matplotlib import pylab as plt
from sklearn.ensemble import RandomForestRegressor


def read_data():
    URL = "https://drive.google.com/uc?id=1MZMKbSQXeVnlAWijTC_hwFCCxPbYNX-Y"
    r = requests.get(URL)
    row_data = pd.read_csv(io.BytesIO(r.content))

    # float型にしないとモデルを推定する際にエラーがでる
    row_data.earnings = row_data.earnings.astype('float64')
    row_data.temperature = row_data.temperature.astype('float64')
    # datetime型にしてインデックスにする
    row_data.date = pd.to_datetime(row_data.date)
    data = row_data.set_index('date')
    return data


def vizualize_ts(data):
    plt.plot(data.earnings)
    plt.show()

    #  自己相関のグラフ
    fig = plt.figure(figsize=(12,8))

    # 水色になっている部分は95％信頼区間を表す。この信頼区間外にデータが及んでいる点は統計的に有意差があると言える。
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(data.earnings, lags=40, ax=ax1)  # plot_acf:コレログラム
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(data.earnings, lags=40, ax=ax2)  # plot_pacf:偏自己相関
    plt.show()

    # データをトレンドと季節成分に分解
    seasonal_decompose_res = sm.tsa.seasonal_decompose(data.earnings, freq=12)
    seasonal_decompose_res.plot()
    plt.show()

    # データを定常にする（処理前） ###############
    # トレンド項あり（１次まで）、定数項あり
    ct = sm.tsa.stattools.adfuller(data.earnings, regression="ct")
    # トレンド項なし、定数項あり
    c = sm.tsa.stattools.adfuller(data.earnings, regression="c")
    # トレンド項なし、定数項なし
    nc = sm.tsa.stattools.adfuller(data.earnings, regression="nc")
    print('----P値を棄却できないため、非定常である----')
    print("ct:")
    print(ct[1])
    print('--------')
    print("c:")
    print(c[1])
    print('--------')
    print("nc:")
    print(nc[1])
    print('--------')

    # データを定常にする ##################
    diff = data.earnings.diff()
    diff = diff.dropna()

    # トレンド項あり（１次まで）、定数項あり
    ct = sm.tsa.stattools.adfuller(diff, regression="ct")
    # トレンド項なし、定数項あり
    c = sm.tsa.stattools.adfuller(diff, regression="c")
    # トレンド項なし、定数項なし
    nc = sm.tsa.stattools.adfuller(diff, regression="nc")

    print('----P値を棄却できるため、非定常でない。----')
    print("ct:")
    print(ct[1])
    print('--------')
    print("c:")
    print(c[1])
    print('--------')
    print("nc:")
    print(nc[1])
    print('--------')

    plt.plot(diff)
    plt.show()


def main():
    # データ読み込み
    data = read_data()

    # 時系列データ可視化
    vizualize_ts(data)


if __name__ == '__main__':
    print('main---start')
    main()
