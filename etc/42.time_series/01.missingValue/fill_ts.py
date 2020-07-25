import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_date():
    df = pd.read_csv('./input_data/input_date.csv')
    df['t'] = pd.to_datetime(df['t'])
    df.set_index('t', inplace=True)
    return df


def date():
    # 方法1
    print('方法1------start')
    df = read_date()
    df = df.interpolate()
    print(df)

    # 方法2
    print('方法2------start')
    df = read_date()
    df = df.interpolate('time')
    print(df)

    # 方法3
    print('方法3------start')
    new_idx = pd.date_range(df.index[0], df.index[-1], freq='D')
    df = df.reindex(new_idx, fill_value=np.nan)
    df = df.interpolate()
    print(df)


def read_sec():
    df = pd.read_csv('./input_data/input_sec.csv')
    df['t'] = pd.to_datetime(df['t'])
    df.set_index('t', inplace=True)
    return df


def sec():
    # 方法1
    print('方法1------start')
    df = read_sec()
    df = df.interpolate()
    print(df)
    df['v1'].plot()
    plt.show()

    # 方法2
    print('方法2------start')
    df = read_sec()
    df = df.interpolate('time')
    print(df)

    # 方法3
    print('方法3------start')
    new_idx = pd.date_range(df.index[0], df.index[-1], freq='1min')
    df = df.reindex(new_idx, fill_value=np.nan)
    df = df.interpolate()
    print(df)


def main():
    print('date------------start')
    date()
    print('sec------------start')
    sec()


if __name__ == '__main__':
    print('main------------------start')
    main()
