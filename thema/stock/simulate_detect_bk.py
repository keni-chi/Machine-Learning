import pandas as pd
from sklearn.linear_model import LinearRegression
import time

import simulate_conf


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
        loop_times = len(df_raw) - simulate_conf.DATASET_DAYS + 1
        df_coef = pd.DataFrame(columns=['Date', '2w', '1m', '6m', '2y'])
        for i in range(loop_times):
            # print(f'---loop_{i}---')
            df = df_raw[i:i+simulate_conf.DATASET_DAYS]
            # print(df)

            # 末尾の日付を取得
            tail_date = df.tail(1)['Date'].values[0]
            # print(tail_date)

            # 関数：dfを入力し、単回帰のaを計算を出力
            df_2week = df.tail(5*2)
            a_2week = self.simple_reg(df_2week)

            df_1month = df.tail(5*4)
            a_1month = self.simple_reg(df_1month)

            df_6month = df.tail(5*4*6)
            a_6month = self.simple_reg(df_6month)

            df_2year = df.tail(5*4*12*2)
            a_2year = self.simple_reg(df_2year)

            df_temp = pd.DataFrame(
                {
                 'Date': [tail_date],
                 '2w': a_2week, 
                 '1m': a_1month, 
                 '6m': a_6month, 
                 '2y': a_2year}
            )

            # 末尾の日付とaをdfのレコードとして追加
            df_coef = pd.concat([df_coef, df_temp])

        # 出力
        df_coef.to_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_coef.csv', encoding='shift-jis')

        return df_coef

    def buy_flg(self, df):
        print(df)
        df_filter = df[
            (df['2w']>0)
            &(df['1m']>0)
            &(df['6m']>0)
            &(df['2y']>0)]
        df_filter['flg'] = 1
        df_filter = df_filter[['Date', 'flg']]

        # 1度フラグが立つと、最低4日空ける
        for i in range(1,5):
            col_name = 'back_' + str(i)
            df_filter[col_name] = df_filter['flg'].shift(1)


        df_buy = pd.merge(df, df_filter, on='Date', how='left')
        # 出力
        df_buy.to_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_buy.csv', encoding='shift-jis')

    def run(self):
        # 係数のデータセットを作成
        df_coef = self.calc_coef()
        # # debug
        # time.sleep(2)
        # df_coef = pd.read_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_coef.csv', index_col=0, encoding='shift-jis')
        # print('aa')
        # print(df_coef)

        # 購入用のフラグを立てる
        self.buy_flg(df_coef)



