import glob
import pandas as pd
import os
import datetime as dt


def make_max():
    path_list = glob.glob('./data/*.csv')
    print(path_list)
    df_dataset = pd.DataFrame()
    code_list = []
    max_list = []

    for path in path_list:
        try:
            # print(path)
            df = pd.read_csv(path)
            if len(df) == 0:
                continue
            df['Date'] = pd.to_datetime(df['Date'])

            # # 日付絞り込み
            # df = df[df['Date'] > dt.datetime(2018,1,1)]
            # df = df[df['Date'] < dt.datetime(2023,5,1)]

            # 株価絞り込み
            df_temp =df.copy()
            df_temp = df_temp[df_temp['Date'] > dt.datetime(2023,4,20)]
            df_temp = df_temp[df_temp['Close'] < 5000]
            if len(df_temp)==0:
                # print('5000円以上なのでskip')
                continue

            # 1カ月max
            df = df.set_index('Date')
            df_m = df.resample('M').max()

            # 1カ月前～12カ月前のmaxのmaxを列追加
            df_m['1カ月前～12カ月前のmaxのmax'] = df_m['Close'].rolling(12).max().shift(1)
            # print(df_m.tail(15))

            # 現在月のmaxが12カ月前までのmaxよりXX倍以上ならtrue
            df_m['xx倍'] = df_m['Close'] > df_m['1カ月前～12カ月前のmaxのmax'] *1.5
            df_m['倍率'] = df_m['Close'] / df_m['1カ月前～12カ月前のmaxのmax']
            # print(df_m.head(30))
            any_flg = any(df_m['xx倍'].tolist())
            if not any_flg:
                # print('急上昇なし')
                continue

            # code
            code = path.split('_')[1].split('.')[0]
            print(code)
            code_list.append(code)

            # 倍率を計算
            max_v = df_m['倍率'].max()
            max_list.append(max_v)
        except Exception as e:
            pass
            # print(e)
            # print('skip')

    # 出力
    df_dataset['コード'] = code_list
    df_dataset['倍率'] = max_list
    df_dataset = df_dataset.sort_values(by=['倍率'], ascending=False)
    df_dataset.to_csv(os.path.dirname(__file__) + '/max/data_max1.csv', encoding='shift_jis')

    return df_dataset


def main():
    df_dataset = make_max()


if __name__ == '__main__':
    main()