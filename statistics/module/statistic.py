import pandas as pd
import scipy.stats as st
# import matplotlib.pyplot as plt
# import math
# import numpy as np


class StatisticalTests():
    def __init__(self):
        pass

    def basic_info(self, df):
        print('基本統計量------------------start')
        print('df.head(3)-------------')
        print(df.head(3))
        print('df.dtypes-------------')
        print(df.dtypes)
        print('df.describe(include=\'all\')-------------')
        print(df.describe(include='all'))

    def shapiro(self, df):
        print('シャピロ・ウィルク検定(データの正規性の統計検定)------------------start')

        dt = ['int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32',
              'uint64', 'float16', 'float32', 'float64', 'float128']
        df_list = []
        for d in dt:
            df_list.append(df.select_dtypes(include=d))

        for i, df in enumerate(df_list):
            if i == 0:
                df_con = df
            else:
                df_con = pd.concat([df_con, df], axis=1)

        for column_name, item in df_con.iteritems():
            _, p = st.shapiro(item)
            if p >= 0.05:
                print(f'カラム名 = {column_name} // p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、正規性あり')
            else:
                print(f'カラム名 = {column_name} // p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、正規性なし')


df = pd.read_csv('./input.csv')
s = StatisticalTests()
s.basic_info(df)
s.shapiro(df)
