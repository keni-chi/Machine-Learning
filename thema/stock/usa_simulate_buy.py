import pandas as pd
import time

import simulate_conf



class Buy():

    def __init__(self, df_raw, code):
        self.df_raw = df_raw
        self.code = code


    def run(self):
        # df_buyを読み込み
        df_buy = pd.read_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_buy.csv', index_col=0, encoding='shift-jis')

        # df_buyのflgで1が立っている日付の、次の日付のリストを取得
        df_flg = df_buy.copy()
        df_flg['flg'] = df_flg['flg'].shift(1)
        df_flg = df_flg[df_flg['flg']==1]
        df_flg = df_flg[['Date']]

        # 取得した日付リストの始値を取得可能なdfを出力
        df_start = pd.merge(df_flg, self.df_raw, on='Date', how='left')
        df_start = df_start[['Date', 'Open']]
        df_start.to_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_start.csv', encoding='shift-jis')
