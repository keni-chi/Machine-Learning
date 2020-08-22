# 基本のライブラリを読み込む
import numpy as np
import pandas as pd
from scipy import stats

# グラフ描画
from matplotlib import pylab as plt
import seaborn as sns

# グラフを横長にする
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

# 統計モデル
import statsmodels.api as sm



def read_data():
    # 日付形式で読み込む
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
    df = pd.read_csv('input_data/AirPassengers.csv', index_col='Month', date_parser=dateparse, dtype='float')
    print(df.head())

    # 日付形式にする
    ts = df['#Passengers'] 
    print(type(ts.head()))

    # プロット
    plt.plot(ts)
    plt.show()
    return ts


def predict_local(ts):
    # ローカルレベルモデルの推定
    mod_local_level = sm.tsa.UnobservedComponents(ts, 'local level')

    # 最尤法によるパラメタの推定
    res_local_level = mod_local_level.fit()

    # 推定されたパラメタ一覧
    print(res_local_level.summary())

    # # 推定された状態・トレンドの描画
    # rcParams['figure.figsize'] = 15, 15
    # fig = res_local_level.plot_components()
    # plt.show()
    return res_local_level


def predict_trend(ts):
    # ローカル線形トレンドモデル
    mod_trend = sm.tsa.UnobservedComponents(ts, 'local linear trend')

    # 最尤法によるパラメタの推定
    # ワーニングが出たのでBFGS法で最適化する
    res_trend = mod_trend.fit(method='bfgs')

    # 推定されたパラメタ一覧
    print(res_trend.summary())

    # # 推定された状態・トレンドの描画
    # rcParams['figure.figsize'] = 15, 20
    # fig = res_trend.plot_components()
    # plt.show()
    return res_trend


def predict_season(ts):
    # 季節変動ありのローカルレベルモデル
    mod_season_local_level = sm.tsa.UnobservedComponents(
        ts,
        'local level',
        seasonal=12
    )

    # まずはNelder-Meadでパラメタを推定し、その結果を初期値としてまた最適化する。2回目はBFGSを使用。
    res_season_local_level = mod_season_local_level.fit(
        method='bfgs', 
        maxiter=500, 
        start_params=mod_season_local_level.fit(method='nm', maxiter=500).params,
    )

    # 推定されたパラメタ一覧
    print(res_season_local_level.summary())

    # # 推定された状態・トレンド・季節の影響の描画
    # rcParams['figure.figsize'] = 15, 20
    # fig = res_season_local_level.plot_components()
    # plt.show()
    return res_season_local_level


def predict_trend_season(ts):
    # 季節変動ありのローカル線形トレンドモデル
    mod_season_trend = sm.tsa.UnobservedComponents(
        ts,
        'local linear trend',
        seasonal=12
    )

    # まずはNelder-Meadでパラメタを推定し、その結果を初期値としてまた最適化する。2回目はBFGSを使用。
    res_season_trend = mod_season_trend.fit(
        method='bfgs', 
        maxiter=500, 
        start_params=mod_season_trend.fit(method='nm', maxiter=500).params,
    )

    # 推定されたパラメタ一覧
    print(res_season_trend.summary())

    # # 推定された状態・トレンド・季節の影響の描画
    # rcParams['figure.figsize'] = 15, 20
    # fig = res_season_trend.plot_components()
    # plt.show()
    return res_season_trend


def mod_season_trend_d(ts):
    # 季節変動ありのローカル線形トレンドモデル
    # ただし、トレンドの分散は無し
    mod_season_trend_d = sm.tsa.UnobservedComponents(
        ts,
        'local linear deterministic trend',  # 変更点
        seasonal=12
    )

    # まずはNelder-Meadでパラメタを推定し、その結果を初期値としてまた最適化する。2回目はBFGSを使用。
    res_season_trend_d = mod_season_trend_d.fit(
        method='bfgs', 
        maxiter=500, 
        start_params=mod_season_trend_d.fit(method='nm', maxiter=500).params,
    )

    # 推定されたパラメタ一覧
    print(res_season_trend_d.summary())

    # # 推定された状態・トレンド・季節の影響の描画
    # rcParams['figure.figsize'] = 15, 20
    # fig = res_season_trend_d.plot_components()
    # plt.show()
    return res_season_trend_d


def res_season_rw(ts):
    # 季節変動ありのローカル線形トレンドモデル
    # ただし、トレンドと観測誤差の分散は無し
    mod_season_rw = sm.tsa.UnobservedComponents(
        ts,
        'random walk with drift',  # 変更点
        seasonal=12
    )

    # まずはNelder-Meadでパラメタを推定し、その結果を初期値としてまた最適化する。2回目はBFGSを使用。
    res_season_rw = mod_season_rw.fit(
        method='bfgs', 
        maxiter=500, 
        start_params=mod_season_rw.fit(method='nm', maxiter=500).params,
    )

    # 推定されたパラメタ一覧
    print(res_season_rw.summary())

    # # 推定された状態・トレンド・季節の影響の描画
    # rcParams['figure.figsize'] = 15, 20
    # fig = res_season_rw.plot_components()
    # plt.show()
    return res_season_rw


def compare_model(model_list):
    # 今まで計算してきたモデルのAICを格納する
    aic_list = pd.DataFrame([], columns=["model", "aic"], index=range(len(model_list)))

    for i, m in enumerate(model_list):
        add_row = [i, m.aic]
        aic_list.iloc[i,:] = add_row

    # 結果の表示
    aic_list['aic'] = pd.to_numeric(aic_list['aic'])
    print(aic_list)
    model_index = aic_list['aic'].idxmin()
    return model_index


def main():
    ts = read_data()
 
    m1 = predict_local(ts)
    m2 = predict_trend(ts)
    m3 = predict_season(ts)
    m4 = predict_trend_season(ts)
    m5 = mod_season_trend_d(ts)
    m6 = res_season_rw(ts)

    model_list = [m1, m2, m3, m4, m5, m6]
    model_index = compare_model(model_list)

    # 予測
    pred = model_list[model_index].predict('1960-01-01', '1961-12-01')
    # 実データと予測結果の図示
    rcParams['figure.figsize'] = 15, 6
    plt.plot(ts)
    plt.plot(pred, "r")
    plt.show()


if __name__ == '__main__':
    print('main---start')
    main()
