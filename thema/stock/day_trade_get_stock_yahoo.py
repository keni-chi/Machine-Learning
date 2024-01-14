import os
import datetime as dt
from datetime import datetime
import time
import sys
import pandas as pd
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import simulate_conf

# コード
data_j  = pd.read_csv('data_j_prime.csv', usecols=[0, 1], encoding='shift_jis')
print(data_j )
target_no_list = data_j ['コード'].tolist()

#2022-01-01以降の株価取得
start='2023-12-01'
end = dt.date.today()

# フォルダ作成
SAMPLE_DIR = f'data-yahoo-day-trade-{simulate_conf.RUNDATE}'
if not os.path.exists(SAMPLE_DIR):
    # ディレクトリが存在しない場合、ディレクトリを作成する
    os.makedirs(SAMPLE_DIR)


def get_stock_data():
    stock_info = None
    for code in target_no_list:
        print(f'---{str(code)}---')
        # 続きのコードからdownload設定
        if code <= 0:  #4021
            continue

        try:
            sharedata = share.Share(f'{code}.T')
            symbol_data=None
            symbol_data = sharedata.get_historical(share.PERIOD_TYPE_DAY, 7, share.FREQUENCY_TYPE_MINUTE, 1)
            tmp = pd.DataFrame(symbol_data)

            data = tmp['timestamp']
            tmp['timestamp'] = [datetime.utcfromtimestamp(int(data[i]/1000)) for i in range(len(data))]

            tmp = tmp.rename(columns={
                'timestamp': 'timestamp',
                'code': 'code',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })
            tmp = tmp.set_index('timestamp')
            tmp.to_csv(f'./data-yahoo-day-trade-{simulate_conf.RUNDATE}/stock_'+ str(code) + '.csv')
        except:
            print(f'---エラー:{str(code)}---')



def main():
    get_stock_data()


if __name__ == '__main__':
    main()