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

sub_folder = 'processed'


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


def to_day():
    # 対象外銘柄の抽出
    df_del = pd.read_csv('./data_j_prime.csv', encoding='shift_jis')
    # df_del = df_del[(df_del['市場・商品区分']=='プライム（内国株式）')|(df_del['市場・商品区分']=='スタンダード（内国株式）')|(df_del['市場・商品区分']=='グロース（内国株式）')]
    df_del = df_del[(df_del['市場・商品区分']!='プライム（内国株式）')&(df_del['市場・商品区分']!='スタンダード（内国株式）')&(df_del['市場・商品区分']!='グロース（内国株式）')]
    del_code_list = df_del['コード'].astype('str').tolist()
    print('A001')
    print(del_code_list)

    path_list = glob.glob('./data-yahoo-20230927/*.csv')
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
    # df_dataset.to_csv(f'{sub_folder}/df_test.csv', encoding='shift_jis')

    df_dataset = drop_manyNuNcolumns(df_dataset, 0.2)

    # 補間
    df_dataset = df_dataset.interpolate()
    df_dataset = df_dataset.fillna(method='ffill') # 直前の値
    df_dataset = df_dataset.fillna(method='bfill') # 直後の値
    df_dataset.to_csv(f'{sub_folder}/df_test2.csv', encoding='shift_jis')

    # # 日付絞り込み
    # df_dataset['Date'] = pd.to_datetime(df_dataset['Date'])
    # df_dataset = df_dataset[df_dataset['Date'] > dt.datetime(2019,4,30)]
    # # df_dataset = df_dataset[df_dataset['Date'] < dt.datetime(2023,5,1)]

    # # 株価絞り込み
    # df_temp =df_dataset.copy()
    # df_temp = df_temp[df_temp['Date'] >= dt.datetime(2023,9,1)]
    # df_temp.drop('Date', axis=1, inplace=True)
    # s_temp = df_temp.max()
    # s_temp = s_temp[s_temp < 4000]
    # print('B001')
    # print(s_temp)
    # filter_code_list = s_temp.index.tolist()
    # print('B002')
    # print(filter_code_list)
    # filter_code_list.append('Date')
    # df_dataset = df_dataset[filter_code_list]
    

def main():
    to_day()


if __name__ == '__main__':
    main()
