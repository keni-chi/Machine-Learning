import os
import pandas as pd
import time
import glob
from sklearn.linear_model import LinearRegression
import time

import d_simulate_conf


root_folder = f'./d_reg_{d_simulate_conf.RUNDATE}'
if not os.path.exists(root_folder):
    os.makedirs(root_folder)


def simple_reg(df):
    X = pd.DataFrame(data={'x': df.index.tolist()})
    y = df['Close'].tolist()
    model_lr = LinearRegression()
    model_lr.fit(X, y)
    a = model_lr.coef_
    return a


def calc_coef(df, code):
    df = df.reset_index()
    # 関数：dfを入力し、単回帰のaを計算を出力
    a_1week = simple_reg(df)

    return a_1week


def calc_run(code_list):
    count = 0
    df_coef = pd.DataFrame(columns=['コード', 'a_1week'])

    for code in code_list:
        print(f'---{str(code)}---')
        # # 続きのコードから
        # if code <= 9900:  #4021
        #     continue

        try:
            df = pd.read_csv(f'./data-yahoo-day-trade-{d_simulate_conf.RUNDATE}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')
            # 10~27万に絞り込み
            tail_value = df.tail(1)['Close'].tolist()[0]
            if not (tail_value >=1000)&(tail_value <=2700):
                print('10~27万の範囲外')
                continue
            count += 1

            # 欠損値の補完
            df = df.interpolate()
            df = df.fillna(method='ffill') # 直前の値
            df = df.fillna(method='bfill') # 直後の値

            # 係数の計算
            a = calc_coef(df, code)
            df_temp = pd.DataFrame(data={
                'コード': code,
                'tail_value': tail_value,
                'a_1week': a
            })

            # 保存
            df_coef = pd.concat([df_coef, df_temp])

        except:
            continue

    df_j_prime = pd.read_csv('./data_j_prime.csv', encoding='shift_jis')
    df_coef = pd.merge(df_coef, df_j_prime, on='コード', how='left')

    # 出力
    print(count)
    df_coef.to_csv( f'./d_reg_{d_simulate_conf.RUNDATE}/df_coef.csv', encoding='shift-jis')

    # 傾きで絞り込み
    df_coef_up = df_coef[df_coef['a_1week'] >0]
    print(len(df_coef_up))
    df_coef_up.to_csv( f'./d_reg_{d_simulate_conf.RUNDATE}/df_coef_up.csv', encoding='shift-jis')


def main():
    # codeリストを取得
    df_j_prime = pd.read_csv('./data_j_prime.csv', encoding='shift_jis')
    print(df_j_prime)
    df_code = df_j_prime[(df_j_prime['規模区分'] == 'TOPIX Large70')|(df_j_prime['規模区分'] == 'TOPIX Mid400')|(df_j_prime['規模区分'] == 'TOPIX Small 1')]
    print(df_code)
    code_list = df_code['コード'].tolist()
    print(f'コードのリスト長： {len(code_list)}')

    # 計算実行
    calc_run(code_list)




if __name__ == '__main__':
    main()
