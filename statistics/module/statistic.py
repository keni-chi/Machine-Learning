import math
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np

class StatisticalTests():
    """ネットワーク."""

    def __init__(self):
        """コンストラクタ."""
        pass

    def basic_info(self, df):
        """基本統計量."""
        print('df.head(3)------------------')
        print(df.head(3))
        print('df.dtypes------------------')
        print(df.dtypes)
        print('df.describe(include=\'all\')------------------')
        print(df.describe(include='all'))

    def shapiro(self, df):
        print('シャピロ・ウィルク検定(データの正規性の統計検定)------------------')
        # TODO: 数値列のみ抽出

        for column_name, item in df.iteritems():
            # # print('------column_name, item------')
            # print(type(column_name))
            # print(column_name)
            # print(type(item))
            # print(item)
            # # print('======\n')

            _, p = st.shapiro(item)
            if p >= 0.05:
                print(f'{item} // p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、正規性あり')
            else:
                print(f'{item} // p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、正規性なし')




df = pd.read_csv('./input.csv')
s = StatisticalTests()
s.basic_info(df)
s.shapiro(df)

