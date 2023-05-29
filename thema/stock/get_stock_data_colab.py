!pip install pandas
!pip install pandas_datareader

import os
import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import time
from google.colab import drive

# コード
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/kabu/input/data_j.csv', usecols=[0, 1], encoding='shift_jis')
print(df)
target_no_list = df['コード'].tolist()

#2022-01-01以降の株価取得
start='2022-04-01'
end = dt.date.today()


def get_stock_data():
    for ticker_symbol in target_no_list:
        # 続きのコードからdownload設定
        if ticker_symbol <= 3271:  ##2354,3271
            continue
        if ticker_symbol >= 5000:
            continue

        print(ticker_symbol)

        # コード
        ticker_symbol=str(ticker_symbol)
        ticker_symbol_dr=ticker_symbol + ".JP"

        #データ取得
        df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
        #2列目に銘柄コード追加
        df.insert(0, "code", ticker_symbol, allow_duplicates=False)
        #csv保存
        df.to_csv('/content/drive/MyDrive/kabu/output/stock_'+ ticker_symbol + '.csv')

        time.sleep(2)



def main():
    get_stock_data()


if __name__ == '__main__':
    main()