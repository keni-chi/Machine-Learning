from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import glob
import datetime as dt


def drop_manyNuNcolumns(df, rate):
    # Nanだけでなく無限大,マイナス無限大をNanに直し、欠損とカウントさせる
    df = df.replace([np.inf, -np.inf], np.nan)

    # 各列ごとに、8割欠損がある列を削除
    for col in df.columns:
        # nanになっている行数をカウント
        nans = df[col].isnull().sum()

        # nan行数を全体の行数で割り、8割欠損している列(col)にのみ処理
        if nans / len(df) > rate: 
            # 8割欠損列を削除
            print("drop", col)
            df.drop(col, axis=1, inplace=True)
    return df


def custer_kmeans_day():
    # 対象外銘柄の抽出
    df_del = pd.read_csv('./data_j.csv', encoding='shift_jis')
    # df_del = df_del[(df_del['市場・商品区分']=='プライム（内国株式）')|(df_del['市場・商品区分']=='スタンダード（内国株式）')|(df_del['市場・商品区分']=='グロース（内国株式）')]
    df_del = df_del[(df_del['市場・商品区分']!='プライム（内国株式）')&(df_del['市場・商品区分']!='スタンダード（内国株式）')&(df_del['市場・商品区分']!='グロース（内国株式）')]
    del_code_list = df_del['コード'].astype('str').tolist()
    print('A001')
    print(del_code_list)

    path_list = glob.glob('./dataraw/*.csv')
    print('A002')
    print(len(path_list))

    del_path_list = []
    for p in path_list:
        for c in del_code_list:
            if c in p:
                del_path_list.append(p)
                continue
    path_list = [i for i in path_list if i not in del_path_list]
    print(len(path_list))

    df_dataset = pd.DataFrame()

    for path in path_list:
        # code
        code = path.split('_')[1].split('.')[0]
        print(code)

        df = pd.read_csv(path)
        if len(df) == 0:
            continue

        if len(df_dataset) ==0:
            df_dataset = df[['Date', 'Close']].copy()
            df_dataset = df_dataset.rename(columns={'Close': code})
            continue

        df = df[['Date', 'Close']]
        df = df.rename(columns={'Close': code})
        df_dataset = pd.merge(df_dataset, df, on='Date', how='left')
    print(df_dataset)
    df_dataset.to_csv('kmeans_day/df_test.csv', encoding='shift_jis')

    df_dataset = drop_manyNuNcolumns(df_dataset, 0.2)

    # 日付絞り込み
    df_dataset['Date'] = pd.to_datetime(df_dataset['Date'])
    df_dataset = df_dataset[df_dataset['Date'] > dt.datetime(2019,3,31)]
    df_dataset = df_dataset[df_dataset['Date'] < dt.datetime(2023,4,1)]

    # 補間
    df_dataset = df_dataset.interpolate()
    df_dataset = df_dataset.fillna(method='ffill') # 直前の値
    df_dataset = df_dataset.fillna(method='bfill') # 直後の値

    # 株価絞り込み
    df_temp =df_dataset.copy()
    df_temp = df_temp[df_temp['Date'] >= dt.datetime(2023,3,1)]
    df_temp.drop('Date', axis=1, inplace=True)
    s_temp = df_temp.max()
    s_temp = s_temp[s_temp < 4000]
    print('B001')
    print(s_temp)
    filter_code_list = s_temp.index.tolist()
    print('B002')
    print(filter_code_list)
    filter_code_list.append('Date')
    df_dataset = df_dataset[filter_code_list]

    df_dataset.to_csv('kmeans_day/df_test2.csv', encoding='shift_jis')
    
    df_dataset = df_dataset.set_index('Date')
    # df_dataset.drop('Date', axis=1, inplace=True)
    X = df_dataset.T
    print('A001')
    print(X)
    print(X.info())

    # 標準化
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)
    print('X_std')
    print(X_std)


    # 構築
    n_clusters = 50
    km = KMeans(n_clusters=n_clusters,    # クラスターの個数
                init='k-means++',        # セントロイドの初期値をランダムに設定
                n_init=10,               # 異なるセントロイドの初期値を用いたk-meansあるゴリmズムの実行回数
                max_iter=300,            # k-meansアルゴリズムの内部の最大イテレーション回数
                tol=1e-04,               # 収束と判定するための相対的な許容誤差
                random_state=0)          # セントロイドの初期化に用いる乱数発生器の状態
    y_km = km.fit_predict(X_std)

    # codeとクラスタの対応
    df_map = X.copy()
    df_map['class'] = y_km
    df_map = df_map[['class']]
    df_map_csv = df_map.reset_index()
    print(df_map_csv)
    df_map_csv = df_map_csv.rename({'index': 'コード'}, axis=1)
    df_map_csv['コード'] = df_map_csv['コード'].astype(int)
    print(df_map_csv)
    print(df_map_csv.info())
    df_ext = pd.read_csv('./data_j.csv', encoding='shift_jis')
    print(df_ext)
    print(df_ext.info())
    df_ext = pd.merge(df_ext, df_map_csv, on='コード', how='inner')
    df_ext.to_csv(os.path.dirname(__file__) + '/kmeans_day/df_ext.csv', encoding='shift_jis')


    # グラフ描画
    df_plt = X.T
    # print(df_plt)
    for n_cluster in range(n_clusters):
        # print(n_cluster)
        df_target = df_map[df_map['class'] == n_cluster]
        code_list = df_target.index.tolist()
        # print(code_list)

        # クラスタ毎に絞り込み
        df_clster_n = df_plt[code_list]
        # print('A01')
        # print(df_clster_n)


        df_clster_n.plot()
        plt.savefig(f'kmeans_day/trend/trend_{str(n_cluster)}.png')
        plt.close('all')



def main():
    custer_kmeans_day()


if __name__ == '__main__':
    main()
