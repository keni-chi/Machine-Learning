import os
import datetime as dt
import pandas_datareader.data as web
import pandas as pd

# コード
df = pd.read_csv('data_j.csv', usecols=[0, 1], encoding='shift_jis')
print(df)
target_no_list = df['コード'].tolist()

#2022-01-01以降の株価取得
start='2010-01-01'
end = dt.date.today()


for ticker_symbol in target_no_list:
    # コード
    ticker_symbol=str(ticker_symbol)
    ticker_symbol_dr=ticker_symbol + ".JP"

    #データ取得
    df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
    #2列目に銘柄コード追加
    df.insert(0, "code", ticker_symbol, allow_duplicates=False)
    #csv保存
    df.to_csv( os.path.dirname(__file__) + '/data/stock_'+ ticker_symbol + '.csv')

