import glob
import pandas as pd
import os
import datetime as dt


def make_season():
    path_list = glob.glob('./data_raw/*.csv')
    df_dataset = pd.DataFrame(columns=['Close_updown', 'weekday'])
    code_list = []

    for path in path_list:
        # try:
        # code
        code = path.split('_')[1].split('.')[0]
        code_list.append(code)

        df = pd.read_csv(path)
        if len(df) == 0:
            continue
        df = df[['Date', 'Close']]
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        # updown
        df['Close_1'] = df['Close'].shift(1)
        df = df.dropna()
        df['Close_diff'] = df['Close'] - df['Close_1']
        df['Close_updown'] = 0
        df['Close_updown'] = df['Close_updown'].where(df['Close_diff'] < 0, 1)
        # 曜日
        df['weekday'] = df.index.weekday
        df = df.reset_index(drop=True)
        df = df[['Close_updown', 'weekday']]
        # print(df)
        df_dataset = pd.concat(
            [df_dataset, df],
            axis=0,
            ignore_index=True
        )
    return df_dataset


def main():
    df_dataset = make_season()
    df_dataset.to_csv(os.path.dirname(__file__) + '/weekday/weekday_raw.csv', encoding='shift_jis')
    
    # 曜日ごとに集計
    print(df_dataset)
    df_dataset = df_dataset.set_index(df_dataset['weekday'])
    df_dataset.sort_index(inplace=True)
    df_weekday = df_dataset.groupby(level=0).mean()
    print(df_weekday)
    df_weekday.to_csv(os.path.dirname(__file__) + '/weekday/weekday_ratio.csv', encoding='shift_jis')


if __name__ == '__main__':
    main()