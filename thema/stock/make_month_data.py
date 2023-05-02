import glob
import pandas as pd
import os
import datetime as dt


def make_month():
    path_list = glob.glob('./data/*.csv')
    df_dataset = pd.DataFrame()

    for path in path_list:
        df = pd.read_csv(path)
        if len(df) == 0:
            continue
        df['Date'] = pd.to_datetime(df['Date'])

        # 日付絞り込み
        df = df[df['Date'] > dt.datetime(2018,1,1)]
        df = df[df['Date'] < dt.datetime(2023,5,1)]

        # 株価絞り込み
        df_temp =df.copy()
        df_temp = df_temp[df_temp['Date'] > dt.datetime(2023,4,20)]
        df_temp = df_temp[df_temp['Close'] < 5000]
        if len(df_temp)==0:
            # print('5000円以上なのでskip')
            continue

        # 1カ月平均
        df = df.set_index('Date')
        df_m = df.resample('M').mean()

        # 2年前までで欠損があればskip
        df_2y_check = df_m[df_m.index > dt.datetime(2021,4,30)]
        df_2y_check = df_2y_check.dropna()
        if len(df_2y_check) < 24:
            print('2年前までで欠損があるのでskip')
            continue

        # 2年前より上昇かつ1年前より上昇かつ半年前より上昇
        m_now = df_m[df_m.index == dt.datetime(2023,4,30)]['Close'][0]
        m_halfy = df_m[df_m.index == dt.datetime(2022,10,31)]['Close'][0]
        m_1y = df_m[df_m.index == dt.datetime(2022,4,30)]['Close'][0]
        m_2y = df_m[df_m.index == dt.datetime(2021,4,30)]['Close'][0]
        # 判定
        if (m_now >= m_halfy) and (m_now >= m_1y) and (m_now >= m_2y):
            print('上昇トレンド')
        else:
            # print('上昇トレンドではないのでskip')
            continue

        # 出力
        code = path.split('_')[1].split('.')[0]
        print(code)
        # print(df_m.head())
        df_m.to_csv( os.path.dirname(__file__) + '/data_month/m_stock_'+ code + '.csv')
        df_dataset[code] = df_m['Close']
    return df_dataset


def make_code_list(df_dataset):
    # コード一覧を取得して対象銘柄を絞り込んで出力
    code_list = df_dataset.columns.tolist()
    code_list = [int(i) for i in code_list]
    df = pd.read_csv('data_j.csv', encoding='shift_jis')
    print('A001')
    print(df)
    print(df.info())
    print(code_list)
    df = df[df['コード'].isin(code_list)]
    df.to_csv(os.path.dirname(__file__) + '/dataset/data_j_extract.csv', encoding='shift_jis')


def make_cluster_data(df_dataset):
    # クラスタリング用に出力
    df_dataset = df_dataset.T
    print(df_dataset)
    df_dataset.to_csv(os.path.dirname(__file__) + '/dataset/dataset.csv')


def main():
    df_dataset = make_month()
    make_code_list(df_dataset)
    make_cluster_data(df_dataset)


if __name__ == '__main__':
    main()