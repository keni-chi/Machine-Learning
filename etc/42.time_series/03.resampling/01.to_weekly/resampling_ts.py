import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_sec():
    df = pd.read_csv('input_data/input_sec.csv')
    df['t'] = pd.to_datetime(df['t'])

    # dateだけ取り出すとき
    df['date'] = df['t'].dt.date
    df = df.drop('date', axis=1)

    # datetimeでないとエラーとなる
    df.set_index('t', inplace=True)

    # 週ごとに変換
    df = df.resample('W').sum()
    print(df)

    return df


def main():
    print('sec------------start')
    df = read_sec()
    print(df.dtypes)
    print(df)


if __name__ == '__main__':
    print('main------------------start')
    main()
