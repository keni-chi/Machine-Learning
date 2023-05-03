import glob
import pandas as pd
import os
import datetime as dt


def make_std():
    path_list = glob.glob('./data/*.csv')
    print(path_list)
    df_dataset = pd.DataFrame()
    code_list = []
    diff_per_list = []
    mean_list = []

    for path in path_list:
        try:
            print(path)
            df = pd.read_csv(path)
            if len(df) == 0:
                continue
            df['Date'] = pd.to_datetime(df['Date'])

            # 日付絞り込み
            df = df[df['Date'] > dt.datetime(2023,3,30)]
            df = df[df['Date'] < dt.datetime(2023,5,1)]

            # 株価絞り込み
            df_temp =df.copy()
            df_temp = df_temp[df_temp['Date'] > dt.datetime(2023,4,20)]
            df_temp = df_temp[df_temp['Close'] < 5000]
            if len(df_temp)==0:
                # print('5000円以上なのでskip')
                continue

            # 1カ月前より上昇
            m_now = df[df['Date'] == dt.datetime(2023,4,28)]['Close'].values[0]
            m_1m = df[df['Date'] == dt.datetime(2023,3,31)]['Close'].values[0]
            # 判定
            if m_now >= m_1m:
                print('上昇トレンド')
            else:
                print('上昇トレンドではないのでskip')
                continue

            # code
            code = path.split('_')[1].split('.')[0]
            print(code)
            code_list.append(code)

            # 標準偏差を計算
            std_v = df['Close'].std()
            mean_v = df['Close'].mean()
            diff_per = std_v / mean_v
            # print('A001')
            # print(diff_per)
            diff_per_list.append(diff_per)
            mean_list.append(mean_v)
        except Exception as e:
            print('skip')

    # 出力
    df_dataset['コード'] = code_list
    df_dataset['変化率'] = diff_per_list
    df_dataset['平均'] = mean_list
    df_dataset = df_dataset.sort_values(by=['変化率', '平均'], ascending=False)
    df_dataset.to_csv(os.path.dirname(__file__) + '/std/data_std.csv', encoding='shift_jis')

    return df_dataset


def main():
    df_dataset = make_std()


if __name__ == '__main__':
    main()