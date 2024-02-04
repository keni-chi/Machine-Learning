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
import usa_simulate_conf
import time


simple_reg = f'usa_simple_reg_{usa_simulate_conf.RUNDATE}'
static_month_path = f'usa_static_month_{usa_simulate_conf.RUNDATE}'
if not os.path.exists(static_month_path):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(static_month_path)


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


def static_month():
    # 対象外銘柄の抽出
    # df_del = pd.read_csv('./data_j_prime.csv', encoding='shift_jis')
    # # df_del = df_del[(df_del['市場・商品区分']=='プライム（内国株式）')|(df_del['市場・商品区分']=='スタンダード（内国株式）')|(df_del['市場・商品区分']=='グロース（内国株式）')]
    # df_del = df_del[(df_del['市場・商品区分']!='プライム（内国株式）')&(df_del['市場・商品区分']!='スタンダード（内国株式）')&(df_del['市場・商品区分']!='グロース（内国株式）')]
    # del_code_list = df_del['コード'].astype('str').tolist()
    del_code_list = []
    path_list = glob.glob(f'./usa-data-yahoo-{usa_simulate_conf.RUNDATE}/*.csv')

    del_path_list = []
    for p in path_list:
        for c in del_code_list:
            if c in p:
                del_path_list.append(p)
                continue
    path_list = [i for i in path_list if i not in del_path_list]
    # print(len(path_list))

    df_dataset = pd.DataFrame()

    for path in path_list:
        # code
        code = path.split('_')[1].split('.')[0]
        # print(code)

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
    df_dataset = drop_manyNuNcolumns(df_dataset, 0.2)

    # # 日付絞り込み
    # df_dataset['Date'] = pd.to_datetime(df_dataset['Date'])
    # df_dataset = df_dataset[df_dataset['Date'] > dt.datetime(2023,1,1)]
    # df_dataset = df_dataset[df_dataset['Date'] < dt.datetime(2023,5,1)]

    # 補間
    # time_s = df_dataset['Date']
    # df_dataset = df_dataset.drop('Date', axis=1)
    df_dataset = df_dataset.interpolate()
    df_dataset = df_dataset.fillna(method='ffill') # 直前の値
    df_dataset = df_dataset.fillna(method='bfill') # 直後の値
    df_dataset.to_csv(f'{static_month_path}/df_dataset.csv', encoding='shift_jis')


def calc_month(df):
    df_month = pd.DataFrame(columns=df.columns.tolist())

    for year in range(2013, 2024):
        # print(year)
        pass

        for month in range(1, 13):
            # df_dataset = df_dataset[df_dataset['Date'] < dt.datetime(2023,5,1)]
            latest = f'{str(year)}-{str(month).zfill(2)}-'

            # 各月の先頭の値を取り出す
            print('A0001')
            print(df)
            df_latest = df[df['Date'].str.contains(latest)].head(1)
            # print(df_latest)
            df_month = pd.concat([df_month, df_latest])

    df_month.to_csv(f'{static_month_path}/df_month.csv', encoding='shift_jis')

    # diff
    date_s = df_month['Date']
    df_month = df_month.drop('Date', axis=1)
    df_diff = df_month  - df_month.shift(1)
    df_diff['Date'] = date_s
    df_diff.to_csv(f'{static_month_path}/df_diff.csv', encoding='shift_jis')

    # フラグ
    df_diff = df_diff.dropna()
    date_s = df_diff['Date']
    df_flg = df_diff.drop('Date', axis=1)
    # print(df_flg.info())
    df_flg = df_flg.where(df_flg<0.0, 1)
    df_flg = df_flg.where(df_flg>=0.0, 0)
    df_flg['Date'] = date_s
    df_flg.to_csv(f'{static_month_path}/df_flg.csv', encoding='shift_jis')

    # 月の列を追加
    df_flg = pd.concat([df_flg, df_flg['Date'].str.split('-', expand=True)], axis=1).drop(['Date', 0, 2], axis=1).rename(columns={1: 'month'})
    df_flg['month'] = df_flg['month'].astype(int)
    # print(df_flg)

    # 結合元のdf読み込み
    df_meta = pd.read_csv(f'{simple_reg}/df_dataset.csv', index_col=0, encoding='shift_jis')
    df_meta_up = pd.read_csv(f'{simple_reg}/df_dataset_up.csv', index_col=0, encoding='shift_jis')
    # print(df_meta)

    # 月ごとに集計
    for i in range(1, 13):
        df_month_sum = df_flg[df_flg['month'] ==i].sum()
        # print(df_month_sum)
        df_month_sum = df_month_sum.reset_index().rename(columns={'index': 'コード', 0: str(i)+'月'})
        df_month_sum = df_month_sum[df_month_sum['コード'] != 'month']
        # df_month_sum['コード'] = df_month_sum['コード'].astype(int)
        # 結合
        df_meta = pd.merge(df_meta, df_month_sum, on='コード', how='left')
        df_meta_up = pd.merge(df_meta_up, df_month_sum, on='コード', how='left')
    df_meta.to_csv(f'{static_month_path}/df_meta.csv', encoding='shift_jis')
    df_meta_up.to_csv(f'{static_month_path}/df_meta_up.csv', encoding='shift_jis')

    # ボックス相場の候補絞り込み
    df_box = df_meta_up.copy()
    df_box = df_box[df_box['6month_a'] < df_box['6month_a'].quantile(0.25)]  
    df_box = df_box[df_box['6month_mape'] < df_box['6month_mape'].quantile(0.25)]
    df_box = df_box[df_box['1month_a'] < df_box['1month_a'].quantile(0.25)]  
    df_box = df_box[df_box['1month_mape'] < df_box['1month_mape'].quantile(0.25)]
    df_box.to_csv(f'{static_month_path}/df_box.csv', encoding='shift_jis')

    # 上昇かつボックス相場の候補絞り込み
    df_box_up = df_meta_up.copy()
    df_box_up = df_box_up[df_box_up['6month_a'] > df_box_up['6month_a'].quantile(0.75)]  
    df_box_up = df_box_up[df_box_up['6month_mape'] < df_box_up['6month_mape'].quantile(0.25)]
    df_box_up = df_box_up[df_box_up['1month_a'] > df_box_up['1month_a'].quantile(0.75)]  
    df_box_up = df_box_up[df_box_up['1month_mape'] < df_box_up['1month_mape'].quantile(0.25)]
    df_box_up.to_csv(f'{static_month_path}/df_box_up.csv', encoding='shift_jis')


def calc_weekday(df):
    # diff
    date_s = df['Date']
    df = df.drop('Date', axis=1)
    df_diff = df  - df.shift(1)
    df_diff['Date'] = date_s

    # フラグ
    df_diff = df_diff.dropna()
    date_s = df_diff['Date']
    df_flg = df_diff.drop('Date', axis=1)
    df_flg = df_flg.where(df_flg<0.0, 1)
    df_flg = df_flg.where(df_flg>=0.0, 0)
    df_flg['Date'] = date_s
    df_flg.to_csv(f'{static_month_path}/df_flg.csv', encoding='shift_jis')

    # 曜日列の追加
    df_flg['Date'] = pd.to_datetime(df_flg['Date'], format='%Y-%m-%d')
    df_flg['weekday'] = df_flg['Date'].dt.day_name()
    df_flg = df_flg.set_index('Date')
    # print(df_flg)

    # 結合元のdf読み込み
    df_weekday_meta = pd.read_csv(f'{static_month_path}/df_meta.csv', index_col=0, encoding='shift_jis')
    df_weekday_meta_up = pd.read_csv(f'{static_month_path}/df_meta_up.csv', index_col=0, encoding='shift_jis')

    # 曜日ごとに集計
    for i in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
        df_weekday = df_flg[df_flg['weekday'] ==i]
        days = len(df_weekday)
        df_weekday_sum = df_weekday.sum()
        df_weekday_sum = df_weekday_sum.reset_index().rename(columns={'index': 'コード', 0: i})
        df_weekday_sum = df_weekday_sum[df_weekday_sum['コード'] != 'weekday']
        df_weekday_sum[i] = df_weekday_sum[i]/days
        # df_weekday_sum['コード'] = df_weekday_sum['コード'].astype(int)
        # 結合
        df_weekday_meta = pd.merge(df_weekday_meta, df_weekday_sum, on='コード', how='left')
        df_weekday_meta.to_csv(f'{static_month_path}/df_weekday_meta.csv', encoding='shift_jis')
        df_weekday_meta_up = pd.merge(df_weekday_meta_up, df_weekday_sum, on='コード', how='left')
        df_weekday_meta_up.to_csv(f'{static_month_path}/df_weekday_meta_up.csv', encoding='shift_jis')


def main():
    # データ整形
    print('static_month')
    static_month()
    print('sleep3')
    time.sleep(3)

    # 月の分析
    df = pd.read_csv(f'{static_month_path}/df_dataset.csv', index_col=0, encoding='shift_jis')
    print('A0001')
    print(df)
    calc_month(df)    

    # 曜日の分析
    calc_weekday(df)



if __name__ == '__main__':
    main()
