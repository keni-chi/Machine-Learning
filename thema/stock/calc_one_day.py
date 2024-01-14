from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error as mape
import os
import config


target_buy_list = ['2023-12-04']
target_sale_list = ['2023-12-06', '2023-12-08', '2023-12-13','2023-12-15']


def simulate():
    df_simulate = pd.read_csv(f'simple_reg_{config.RUNDATE}/df_dataset_up.csv', index_col=0, encoding='shift-jis')
    target_code_list = df_simulate['コード'].tolist()
    print(df_simulate)

    for buy in target_buy_list:

        for sale in target_sale_list:
            code_list, buy_list, sale_list, benefit_list, benefit_ratio_list = [], [], [], [], []

            for code in target_code_list:
                df_code = pd.read_csv(f'data-yahoo-{config.SIMULATE_ANSWER}/stock_{str(code)}.csv', index_col=0, encoding='shift-jis')
                # print(df_code.info())


                # buy
                df_buy = df_code[df_code.index == buy]
                buy_value = df_buy['Close'].tolist()[0]

                # sale
                df_sale = df_code[df_code.index == sale]
                sale_value = df_sale['Close'].tolist()[0]

                # benefit
                benefit = sale_value - buy_value
                benefit_ratio = benefit / buy_value

                # append
                code_list.append(code)
                buy_list.append(buy_value)
                sale_list.append(sale_value)
                benefit_list.append(benefit)
                benefit_ratio_list.append(benefit_ratio)

            # 結果保存
            key = buy + ' - ' + sale
            from_to_dict = {
                'コード': code_list,
                'buy'+key : buy_list,
                'sale'+key: sale_list,
                'benefit'+key: benefit_list,
                'benefit_ratio'+key: benefit_ratio_list
            }
            df_result = pd.DataFrame(from_to_dict)
            # print(df_result)
            # df_result['コード'] = df_result['コード'].astype(str)
            df_simulate = pd.merge(df_simulate, df_result, on='コード', how='left')
            df_simulate.to_csv(f'simple_reg_{config.RUNDATE}/df_simulate.csv', encoding='shift-jis')


def main():
    simulate()


if __name__ == '__main__':
    main()
