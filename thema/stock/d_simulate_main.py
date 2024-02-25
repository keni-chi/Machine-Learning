import os
import pandas as pd
import time
import glob

import d_simulate_conf
from d_simulate_detect import Detect
from d_simulate_buy import Buy
from d_simulate_sale import Sale


root_folder = f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}'
if not os.path.exists(root_folder):
    os.makedirs(root_folder)


def calc_run(code_list):
    count = 0
    for code in code_list:  #[1852]:
        print(f'---{str(code)}---')
        count += 1
        print(len(code_list))
        print(count)

        # 生データ読み込み
        try:
            df = pd.read_csv(f'./data-yahoo-day-trade-{d_simulate_conf.RUNDATE}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')
        except:
            continue

        ## 1日毎に分割 #####
        df_code = df.copy()
        df_ts = df.copy()
        ts_list = df_ts.reset_index()['timestamp'].str.split(' ', expand=True)[0].drop_duplicates().tolist()
        print('A001')
        print(ts_list)

        for ts in ts_list:
            print('----')
            print(ts)
            df = df_code[df_code.index.str.contains(ts)]
            print(df)

            # nanの割合が高ければskip
            nans = df['Open'].isnull().sum()
            if nans / len(df) > 0.7: 
                print('取引が少なくcontinue')
                continue

            # コード毎のフォルダ作成
            code_folder = root_folder + '/' + str(code) + '/' + ts
            if not os.path.exists(code_folder):
                os.makedirs(code_folder)

            # 5844でnanエラーの対応
            df = df.interpolate()
            df = df.fillna(method='ffill') # 直前の値
            df = df.fillna(method='bfill') # 直後の値
            # df = df.tail(5*4*12*3)
            
            # 次の日に購入するべき日、を検知
            print('detect---start')
            Detect(df, code, ts).run()
            time.sleep(2)

            # 買う日、その始値、を整理
            print('buy---start')
            Buy(df, code, ts).run()
            time.sleep(2)

            # 売る日、売値、損益額、を整理し、CSV出力
            print('sale---start')
            Sale(df, code, ts).run()
            time.sleep(2)


def aggregate_simulation(code_list, df):
    df_agg = pd.DataFrame()
    for code in code_list:  #[1852]:
        # print('======')
        # print(code)
        #TODO: tsでループを回して、１つのコードに対して損益を1行にまとめる
        # 生データ読み込み
        try:
            df_raw = pd.read_csv(f'./data-yahoo-day-trade-{d_simulate_conf.RUNDATE}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')
        except:
            continue
        ## 1日毎に分割 #####
        df_ts = df_raw.copy()
        ts_list = df_ts.reset_index()['timestamp'].str.split(' ', expand=True)[0].drop_duplicates().tolist()
        # 損益の集計値
        total_soneki = 0

        for ts in ts_list:
            try:
                df_total_soneki = pd.read_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/{str(code)}/{ts}/df_total_soneki.csv', index_col=0, encoding='shift-jis')
                total_soneki_v = df_total_soneki[str(code)].tolist()[0]
                total_soneki = total_soneki + total_soneki_v
            except:
                continue

        df_temp = pd.DataFrame({
            'index': [str(code)],
            'timestamp': ['dummy'],
            'Open': ['dummy'],
            'sale_date': ['dummy'],
            'sale_value': ['dummy'],
            '損益': [total_soneki],
            'days': ['dummy']
        })
        df_temp = df_temp.set_index('index')
        # print('df_temp')
        # print(df_temp)
        # print('--col---')
        # print(df_agg.columns.tolist())
        # print(df_temp.columns.tolist())

        df_agg = pd.concat([df_agg, df_temp], axis=0)
        # print('df_agg')
        # print(df_agg)

    # df_agg = df_agg.T

    df_agg = df_agg.reset_index().rename(columns={'index': 'コード', '損益': 'simulation'})
    df_agg['コード'] = df_agg['コード'].astype(int)
    df_agg = pd.merge(df, df_agg, on='コード', how='left')
    # 出力
    df_agg.to_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/df_agg.csv', encoding='shift-jis')
    time.sleep(2)


def aggregate_accumulation():
    path_list = glob.glob(f'./d_simulate_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
    # path_list = ['./d_simulate_20240208-0.8-0.4']
    # d_simulate_conf.RUNDATE = '20240208-0.8-0.4'
    df_acc = pd.DataFrame({'コード': []})

    for p in path_list:
        yymmdd = p.split('_')[2]
        df = pd.read_csv(f'{p}/df_agg.csv', index_col=0, encoding='shift-jis')
        df = df[['コード', 'simulation']]
        df = df.rename(columns={'simulation': yymmdd})
        df_acc = pd.merge(df_acc, df, on='コード', how='outer')

    df_agg = pd.read_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/df_agg.csv', index_col=0, encoding='shift-jis')
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
    df_acc.to_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/df_acc.csv', encoding='shift-jis')


def main():
    # codeリストを取得
    df = pd.read_csv(f'./d_reg_{d_simulate_conf.RUNDATE}/df_coef_up.csv', index_col=0, encoding='shift-jis')
    # df = pd.read_csv(f'./static_month_{d_simulate_conf.RUNDATE}/df_weekday_meta_up.csv', index_col=0, encoding='shift-jis')
    ###
    df['コード'] = df['コード'].astype(int)
    code_list = df['コード'].tolist()
    code_list = sorted(code_list)
    # code_list = [3167, 7463]

    print('===コードリストの長さ===')
    print(len(code_list))
    print('===コードリストの長さ===')

    # 計算実行
    calc_run(code_list)

    # 計算結果集約
    aggregate_simulation(code_list, df)

    # # 過去の蓄積分を集約
    # aggregate_accumulation()


if __name__ == '__main__':
    main()
