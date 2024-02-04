import pandas as pd
from sklearn.linear_model import LinearRegression
import time

import d_simulate_conf


class Detect():

    def __init__(self, df_raw, code):
        self.df_raw = df_raw
        self.code = code

    def simple_reg(self, df):
        X = pd.DataFrame(data={'x': df.index.tolist()})
        y = df['Close'].tolist()
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a = model_lr.coef_
        return a

    def calc_coef(self):
        df_raw = self.df_raw.reset_index()

        # 6か月分+5日のデータセットのループ(例： 6*20+5=125)
        loop_times = len(df_raw) - d_simulate_conf.DATASET_DAYS + 1
        df_coef = pd.DataFrame(columns=['timestamp', '10m', '20m', '1d', '2d'])
        for i in range(loop_times):
            # print(f'---loop_{i}---')
            df = df_raw[i:i+d_simulate_conf.DATASET_DAYS]
            # print(df)

            # 末尾の日付を取得
            tail_date = df.tail(1)['timestamp'].values[0]
            # print(tail_date)

            # 関数：dfを入力し、単回帰のaを計算を出力
            df_2week = df.tail(10)
            a_2week = self.simple_reg(df_2week)

            df_1month = df.tail(20)
            a_1month = self.simple_reg(df_1month)

            df_6month = df.tail(60*5)
            a_6month = self.simple_reg(df_6month)

            df_2year = df.tail(60*5*2)
            a_2year = self.simple_reg(df_2year)

            df_temp = pd.DataFrame(
                {
                 'timestamp': [tail_date],
                 '10m': a_2week, 
                 '20m': a_1month, 
                 '1d': a_6month, 
                 '2d': a_2year}
            )

            # 末尾の日付とaをdfのレコードとして追加
            df_coef = pd.concat([df_coef, df_temp])

        # 出力
        df_coef.to_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/{str(self.code)}/df_coef.csv', encoding='shift-jis')

        return df_coef

    def buy_flg(self, df):
        # 傾きの条件でフラグを立てる
        df_filter = df[
            (df['10m']>0)
            &(df['20m']>0)
            &(df['1d']>0)
            &(df['2d']>0)]
        # df_filter['flg'] = 1
        df_filter = df_filter.assign(flg=1)
        df_filter = df_filter[['timestamp', 'flg']]
        df_buy = pd.merge(df, df_filter, on='timestamp', how='left')

        # 1度フラグが立つと、最低60分空ける
        for i in range(1,61):
            col_name = 'back_' + str(i)
            df_buy[col_name] = df_buy['flg'].shift(i)
        df_buy = df_buy.fillna(0)
        df_buy['flg_sum'] = df_buy['flg'] - df_buy['back_1'] - df_buy['back_2'] - df_buy['back_3'] - df_buy['back_4']
        # df_buy.flg_sum = df_buy.flg_sum.replace(df_buy.flg_sum <= 0, -1)
        df_buy.loc[df_buy['flg_sum']<=0, 'flg_sum'] = pd.NA
        df_buy['flg'] = df_buy['flg_sum']
        df_buy = df_buy.drop(['back_1', 'back_2', 'back_3', 'back_4', 'flg_sum'], axis=1)

        # 出力
        df_buy.to_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/{str(self.code)}/df_buy.csv', encoding='shift-jis')

    def run(self):
        # 係数のデータセットを作成
        df_coef = self.calc_coef()
        # # debug
        # time.sleep(2)
        # df_coef = pd.read_csv(f'd_simulate_{d_simulate_conf.RUNDATE}/{str(self.code)}/df_coef.csv', index_col=0, encoding='shift-jis')
        # print('aa')
        # print(df_coef)

        # 購入用のフラグを立てる
        self.buy_flg(df_coef)



