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

    # データを定常にする（処理前） ##################
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


def plot_pred_vs_actual(pred, actual):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    ax.scatter(pred,actual)
    ax.set_title('pred vs actual')
    ax.set_xlabel('pred')
    ax.set_ylabel('actual')
    lims = [0, 1600]
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    plt.grid()
    plt.show()


def plot_ts(pred, actual):
    plt.plot(pred, label="pred")
    plt.plot(actual, label="actual")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    # データ読み込み
    data = read_data()

    # 時系列データ可視化
    vizualize_ts(data)

    # データをトレーニングデータとテストデータに分割
    train_data = data[data.index < "2018-06"]
    test_data = data[data.index >= "2018-05"]
    X_train = train_data['temperature'].values.reshape(-1, 1)
    X_test = test_data['temperature'].values.reshape(-1, 1)
    y_train = train_data['earnings'].values
    y_test = test_data['earnings'].values

    # 学習
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # 評価
    print(model.score(X_train, y_train))
    print(model.score(X_test, y_test))

    # 予測
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # pred vs actual
    plot_pred_vs_actual(y_train_pred, y_train)
    plot_pred_vs_actual(y_test_pred, y_test)

    # plot ts
    plot_ts(y_train_pred, y_train)
    plot_ts(y_test_pred, y_test)


if __name__ == '__main__':
    print('main---start')
    main()
