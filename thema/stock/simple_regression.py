from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error as mape
import os
import simulate_conf


sub_folder = f'kmeans{simulate_conf.RUNDATE}'
SAMPLE_DIR = f'simple_reg_{simulate_conf.RUNDATE}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(SAMPLE_DIR)
    os.makedirs(SAMPLE_DIR + '/png')


def fit_predict(df):
    print('B001---')
    print(df)
    df_dataset = pd.DataFrame()

    # df_1week = df.tail(5)
    # df_1week = simple_reg(df_1week)
    # df_dataset['コード'] = df_1week['code']
    # df_dataset['1week'] = df_1week['a']

    interval = '2w'
    df_2week = df.tail(5*2)
    df_2week = simple_reg(df_2week, interval)
    df_dataset['コード'] = df_2week['code']
    df_dataset['2week_a'] = df_2week['a']
    df_dataset['2week_mape'] = df_2week['mape']

    interval = '1m'
    df_1month = df.tail(5*4)
    df_1month = simple_reg(df_1month, interval)
    df_dataset['1month_a'] = df_1month['a']
    df_dataset['1month_mape'] = df_2week['mape']

    interval = '6m'
    df_6month = df.tail(5*4*6)
    df_6month = simple_reg(df_6month, interval)
    df_dataset['6month_a'] = df_6month['a']
    df_dataset['6month_mape'] = df_6month['mape']

    interval = '2y'
    df_2year = df.tail(5*4*12*2)
    df_2year = simple_reg(df_2year, interval)
    df_dataset['2year_a'] = df_2year['a']
    df_dataset['2year_mape'] = df_6month['mape']

    print(df_dataset.info())

    # 結果の結合
    df = pd.read_csv(f'{sub_folder}/df_ext.csv', index_col=0, encoding='shift-jis')
    df['コード'] = df['コード'].astype(str)
    print(df.info())
    df_dataset = pd.merge(df, df_dataset, on='コード', how='left')
    df_dataset.to_csv(f'simple_reg_{simulate_conf.RUNDATE}/df_dataset.csv', encoding='shift-jis')

    # 結果の絞り込み
    df_dataset_up = df_dataset.copy()
    print(df_dataset_up)
    # df_dataset_up = df_dataset_up[df_dataset_up['1week'] > 0]
    df_dataset_up = df_dataset_up[df_dataset_up['2week_a'] > 0]
    df_dataset_up = df_dataset_up[df_dataset_up['1month_a'] > 0]
    df_dataset_up = df_dataset_up[df_dataset_up['6month_a'] > 0]
    df_dataset_up = df_dataset_up[df_dataset_up['2year_a'] > 0]
    df_dataset_up = df_dataset_up.sort_values(by=['2year_mape', '6month_mape', '1month_mape', '2week_mape'])
    df_dataset_up.to_csv(f'simple_reg_{simulate_conf.RUNDATE}/df_dataset_up.csv', encoding='shift-jis')


def simple_reg(df, interval):
    df = df.reset_index(drop=True).drop('Date', axis=1)
    print(df)

    code_list, a_list, b_list, R2_list, mape_list = [], [], [], [], []

    for code, item in df.items():
        X = pd.DataFrame(data={'x': item.index.tolist()})
        y = item.tolist()
        
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a = model_lr.coef_
        b = model_lr.intercept_
        R2 = model_lr.score(X, y)
        y_pred = model_lr.predict(X)
        mape_score = mape(y, y_pred)

        # 結果の保存
        code_list.append(code)
        a_list.append(a[0])
        b_list.append(b)
        R2_list.append(R2)
        mape_list.append(mape_score)

        # グラフ描画
        # plot_scatter(X, y, y_pred, model_lr, mape_score, interval, code)

    # 結果
    df_result = pd.DataFrame({
        'code':code_list,
        'a':a_list,
        'b':b_list,
        'R2':R2_list,
        'mape':mape_list
    })

    # 出力
    df_result.to_csv(f'simple_reg_{simulate_conf.RUNDATE}/df_simple_reg.csv', encoding='shift-jis')

    return df_result


def plot_scatter(X, y, y_pred, model_lr, mape_score, interval, code):
    df_dataset_up = pd.read_csv(f'simple_reg_{simulate_conf.RUNDATE}/df_dataset_up.csv', index_col=0, encoding='shift-jis')
    up_code_list = df_dataset_up['コード'].astype(str).tolist()
    if str(code) in up_code_list:
        fig, ax = plt.subplots(figsize=(8,8))
        ax.plot(X, model_lr.coef_ * X + model_lr.intercept_, label=f'MAPE={mape_score}')
        ax.plot(X, y, 'k.', label='data')
        ax.plot(X, y_pred, 'ro', label='prediction')
        ax.grid(True)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        # plt.savefig(f'simple_reg_{simulate_conf.RUNDATE}/png/{interval}_{str(code)}.png')


def main():
    df = pd.read_csv(f'{sub_folder}/df_test2.csv', index_col=0)
    print(df)
    print(df.info())
    fit_predict(df)


if __name__ == '__main__':
    main()
