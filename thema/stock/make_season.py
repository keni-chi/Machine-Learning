import glob
import pandas as pd
import os
import datetime as dt


def make_season():
    path_list = glob.glob('./data/*.csv')
    print(path_list)
    df_dataset = pd.DataFrame()
    code_list = []

    for path in path_list:
        # try:
        # code
        code = path.split('_')[1].split('.')[0]
        print(code)
        code_list.append(code)

        df = pd.read_csv(path)
        if len(df) == 0:
            continue
        df['Date'] = pd.to_datetime(df['Date'])

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

        # 月ごとの平均と標準偏差
        df_m = df_m.set_index(df_m.index.month)
        df_m.sort_index(inplace=True)
        df_m_mean = df_m.groupby(level=0).mean()

        df_dataset[code] = df_m_mean['Close']
        # except Exception as e:
        #     print('skip')

    # 出力
    df_dataset.to_csv(os.path.dirname(__file__) + '/season/data_season.csv', encoding='shift_jis')

    # code毎の標準偏差を出力
    df_std = pd.DataFrame()
    df_std['std'] = df_dataset.std()
    df_std['mean'] = df_dataset.mean()
    df_std['diff'] = df_std['std']/df_std['mean']
    df_std = df_std.sort_values('diff') 
    df_std.to_csv(os.path.dirname(__file__) + '/season/data_season_std.csv', encoding='shift_jis')

    return df_dataset


def main():
    df_dataset = make_season()


if __name__ == '__main__':
    main()