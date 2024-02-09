import pandas as pd
import time

import d_simulate_conf



class Buy():

    def __init__(self, df_raw, code, ts):
        self.df_raw = df_raw
        self.code = code
        self.ts = ts

    def run(self):
        # df_buyを読み込み
        df_buy = pd.read_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/{str(self.code)}/{self.ts}/df_buy.csv', index_col=0, encoding='shift-jis')

        # df_buyのflgで1が立っている日付の、次の日付のリストを取得
        df_flg = df_buy.copy()
        df_flg['flg'] = df_flg['flg'].shift(1)
        df_flg = df_flg[df_flg['flg']==1]
        df_flg = df_flg[['timestamp']]

        # 取得した日付リストの始値を取得可能なdfを出力
        df_start = pd.merge(df_flg, self.df_raw, on='timestamp', how='left')
        df_start = df_start[['timestamp', 'Open']]
        df_start.to_csv(f'./d_simulate_{d_simulate_conf.RUNDATE}{d_simulate_conf.suffix}/{str(self.code)}/{self.ts}/df_start.csv', encoding='shift-jis')
