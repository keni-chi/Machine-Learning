import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore') # 計算警告を非表示


# data = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/MASS/drivers.csv')
# data.index = data['time']

# # plt.figure(figsize=(15, 5))
# # plt.plot(data.index, data['value'])
# # plt.ylabel('Driver Deaths')
# # plt.title('Deaths of Car Drivers in Great Britain 1969-84')
# # plt.plot()
# # data_d = data['value']


# data.loc[(data['time']>=1983.05), 'seat_belt'] = 1;
# data.loc[(data['time']<1983.05), 'seat_belt'] = 0;
# data.loc[(data['time']>=1974.00), 'oil_crisis'] = 1;
# data.loc[(data['time']<1974.00), 'oil_crisis'] = 0;
# plt.figure(figsize=(15, 5))
# plt.plot(data.index, data['value'])
# plt.ylabel('Driver Deaths')
# plt.title('Deaths of Car Drivers in Great Britain 1969-84')
# plt.plot()
# # plt.show()
# print(data.head)

# df_a = pd.DataFrame({'a': data['value']})
# df_seat_belt = pd.DataFrame({'seat_belt': data['seat_belt']})


def read_data():
    # 日付形式で読み込む
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
    df = pd.read_csv('AirPassengers.csv', index_col='Month', date_parser=dateparse, dtype='float')
    print(df.head())

    # 日付形式にする
    ts = df['#Passengers'] 
    print(type(ts.head()))

    # プロット
    plt.plot(ts)
    # plt.show()
    return ts


def main():
    ts = read_data()
 
 


if __name__ == '__main__':
    print('main---start')
    main()
