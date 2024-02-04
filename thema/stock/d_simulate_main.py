import os
import pandas as pd
import time
import glob

import d_simulate_conf
from d_simulate_detect import Detect
from d_simulate_buy import Buy
from d_simulate_sale import Sale


root_folder = f'd_simulate_{d_simulate_conf.RUNDATE}'
if not os.path.exists(root_folder):
    os.makedirs(root_folder)


def calc_run(code_list):
    for code in code_list:  #[1852]:
        print(f'---{str(code)}---')

        # 生データ読み込み
        df = pd.read_csv(f'./data-yahoo-day-trade-{d_simulate_conf.RUNDATE}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')

        # nanの割合が高ければskip
        nans = df['Open'].isnull().sum()
        if nans / len(df) > 0.2: 
            print('取引が少なくcontinue')
            continue

        # コード毎のフォルダ作成
        code_folder = root_folder + '/' + str(code)
        if not os.path.exists(code_folder):
            os.makedirs(code_folder)

        # 5844でnanエラーの対応
        df = df.interpolate()
        df = df.fillna(method='ffill') # 直前の値
        df = df.fillna(method='bfill') # 直後の値
        # df = df.tail(5*4*12*3)
        
        # 次の日に購入するべき日、を検知
        print('detect---start')
        Detect(df, code).run()
        time.sleep(2)

        # 買う日、その始値、を整理
        print('buy---start')
        Buy(df, code).run()
        time.sleep(2)

        # 売る日、売値、損益額、を整理し、CSV出力
        print('sale---start')
        Sale(df, code).run()
        time.sleep(2)


def aggregate_simulation(code_list, df):
    df_agg = pd.DataFrame()
    for code in code_list:  #[1852]:
        try:
            df_weekday_meta_up = pd.read_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}/{str(code)}/df_total_soneki.csv', index_col=0, encoding='shift-jis')
        except:
            continue
        df_agg = pd.concat([df_agg, df_weekday_meta_up], axis=1)
    df_agg = df_agg.T
    df_agg = df_agg.reset_index().rename(columns={'index': 'コード', 0: 'simulation'})
    df_agg['コード'] = df_agg['コード'].astype(int)
    df_agg = pd.merge(df, df_agg, on='コード', how='left')
    # 出力
    df_agg.to_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/df_agg.csv', encoding='shift-jis')
    time.sleep(2)


def aggregate_accumulation():
    path_list = glob.glob('./d_simulate_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
    df_acc = pd.DataFrame({'コード': []})

    for p in path_list:
        yymmdd = p.split('_')[1]
        df = pd.read_csv(f'{p}/df_agg.csv', index_col=0, encoding='shift-jis')
        df = df[['コード', 'simulation']]
        df = df.rename(columns={'simulation': yymmdd})
        df_acc = pd.merge(df_acc, df, on='コード', how='outer')

    df_agg = pd.read_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/df_agg.csv', index_col=0, encoding='shift-jis')
    df_acc = pd.merge(df_acc, df_agg, on='コード', how='left')
    df_acc = df_acc.set_index('コード')

    # コード情報を追加
    df_temp = df_acc.copy()
    code_list = df_temp.index.tolist()
    cols = df_temp.columns
    data_j = pd.read_csv('data_j_prime.csv', encoding='shift_jis')
    data_j = data_j.set_index('コード')
    df_fill = df_temp.combine_first(data_j)
    df_temp = df_fill.reindex(columns=cols).reset_index()
    # シミュレーション対象のコードに絞り込み
    df_acc = df_temp[df_temp['コード'].isin(code_list)]

    # 出力
    df_acc.to_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/df_acc.csv', encoding='shift-jis')


def main():
    # codeリストを取得
    df = pd.read_csv(f'./static_month_{d_simulate_conf.RUNDATE}/df_weekday_meta_up.csv', index_col=0, encoding='shift-jis')
    # df = pd.read_csv(f'./static_month_{d_simulate_conf.RUNDATE}/df_weekday_meta.csv', index_col=0, encoding='shift-jis')
    df['コード'] = df['コード'].astype(int)
    code_list = df['コード'].tolist()

    # 計算実行
    calc_run(code_list)

    # 計算結果集約
    aggregate_simulation(code_list, df)

    # 過去の蓄積分を集約
    aggregate_accumulation()


if __name__ == '__main__':
    main()
