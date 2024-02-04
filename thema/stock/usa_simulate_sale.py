import pandas as pd
import time
from datetime import timedelta

import simulate_conf



class Sale():

    def __init__(self, df_raw, code):
        self.df_raw = df_raw
        self.code = code


    def run(self):
        # df_startを読み込み
        df_start = pd.read_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_start.csv', index_col=0, encoding='shift-jis')

        # 保管変数
        sale_date_list = []
        sale_value_list = []

        # startのDateでループ
        for d in df_start['Date'].tolist():
            # Openの価格を取得。
            df_raw = self.df_raw.reset_index()
            df_open = df_raw[df_raw['Date'] ==d]
            open_v = df_open['Open'].values[0]
            
            # upは1.1倍、downは0.95倍、で求める。
            up_v = simulate_conf.rikaku_ratio * open_v
            down_v = simulate_conf.songiri_ratio * open_v

            # dより未来のデータにdf_rawを絞り込んで別変数df_futureに格納
            df_future = df_raw.copy()
            df_future['Date'] = pd.to_datetime(df_future['Date'])
            df_future = df_future.set_index('Date')
            df_future = df_future[d:]

            # up: df_futureに対し、Highの値がup以上でフィルタdf_up。先頭日付をup_date変数に格納。
            df_up = df_future[df_future['High'] >= up_v].head(1).reset_index()
            if len(df_up)==0:
                up_date = '該当なし'
            else:
                up_date = df_up['Date'].dt.strftime('%Y-%m-%d').values[0]
            # print('A01')
            # print(up_v)
            # print(df_up)
            # print(up_date)

            # down: df_futureに対し、Lowの値がdown以下でフィルタdf_down。先頭日付をdown_date変数に格納。
            df_down = df_future[df_future['Low'] <= down_v].head(1).reset_index()
            if len(df_down)==0:
                down_date = '該当なし'
            else:
                down_date = df_down['Date'].dt.strftime('%Y-%m-%d').values[0]
            # print('A02')
            # print(down_v)
            # print(df_down)
            # print(down_date)

            # up_dateとdown_dateの古い方を、sale_dateとして採用。（同じ日ならばup_dateとする）
            if up_date != '該当なし':
                up_date_t = time.strptime(up_date, "%Y-%m-%d")
            if down_date != '該当なし':
                down_date_t = time.strptime(down_date, "%Y-%m-%d")

            # 利益確定、損切、どちらのデータもある
            if (up_date != '該当なし')&(down_date != '該当なし'):
                if up_date_t > down_date_t:
                    # print('損切')
                    sale_date = down_date
                    sale_v = down_v
                else:
                    # print('利益確定')
                    sale_date = up_date
                    sale_v = up_v

            # 利益確定のみデータあり
            if (up_date != '該当なし')&(down_date == '該当なし'):
                sale_date = up_date
                sale_v = up_v

            # 損切のみデータあり
            if (up_date == '該当なし')&(down_date != '該当なし'):
                sale_date = down_date
                sale_v = down_v

            # 利益確定、損切、どちらのデータもない
            if (up_date == '該当なし')&(down_date == '該当なし'):
                sale_date = d    # 売買日数の計算のためdを代入し0となるようにする         # '利益確定、損切、どちらもなし'
                sale_v = open_v  # 損益計算時に0にするために代入

            # sale_dateの日付と、up値またはdown値を、それぞれのlist変数に保存
            sale_date_list.append(sale_date)
            sale_value_list.append(sale_v)

        # df_startに対し、2つのリストを列として追加
        df_start['sale_date'] = sale_date_list
        df_start['sale_value'] = sale_value_list
                    
        # vaule値の差を取って、損益列として追加
        df_soneki = df_start.copy()
        df_soneki['損益'] = df_soneki['sale_value'] - df_soneki['Open']

        # 売買にかかった日数を算出
        df_soneki['date1'] = pd.to_datetime(df_soneki['Date'])
        df_soneki['date2'] = pd.to_datetime(df_soneki['sale_date'])
        df_soneki['days'] = (df_soneki['date2'] - df_soneki['date1'])
        df_soneki['days'] = (df_soneki['days'] / timedelta(days=1))
        df_soneki = df_soneki.drop(['date1', 'date2'], axis=1)
        df_soneki.to_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_soneki.csv', encoding='shift-jis')

        # 単純な合計でトータル損益を求めて、csv保存
        total_soneki = df_soneki['損益'].sum()
        df_total_soneki = pd.DataFrame(data={str(self.code): [total_soneki]})
        df_total_soneki.to_csv(f'simulate_{simulate_conf.RUNDATE}/{str(self.code)}/df_total_soneki.csv', encoding='shift-jis')
        print(total_soneki)
