import datetime as dt
import pandas as pd
import yfinance as yf

# コード
data_j  = pd.read_csv('data_j_prime.csv', usecols=[0, 1], encoding='shift_jis')
print(data_j )
target_no_list = data_j ['コード'].tolist()


def get_stock_bs():
    getted_code_list = []
    dy_list = []
    pbr_list = []
    per_list = []
    for code in target_no_list:

        print(f'---{str(code)}---')
        # 続きのコードからdownload設定
        if code <= 0:  #4021
            continue

        try:
            # 情報取得
            ticker_info = yf.Ticker(f"{code}.T")
            info_dict = ticker_info.info
            # 利回りなど
            fiveYearAvgDividendYield = info_dict['fiveYearAvgDividendYield']
            priceToBook = info_dict['priceToBook']
            trailingPE = info_dict['trailingPE']

            getted_code_list.append(code)
            dy_list.append(fiveYearAvgDividendYield)
            pbr_list.append(priceToBook)
            per_list.append(trailingPE)

        except:
            print(f'---エラー:{str(code)}---')

    df = pd.DataFrame(
        data=
        {'code': getted_code_list,
         'fiveYearAvgDividendYield': dy_list,
         'priceToBook': pbr_list,
         'trailingPE': per_list         
         }
    )
    print(df)
    df.to_csv('./stock_bs.csv', )


def main():
    get_stock_bs()


if __name__ == '__main__':
    main()