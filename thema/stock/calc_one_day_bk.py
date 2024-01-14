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


buy = '2023-12-04'
sale = '2023-12-15'


def simulate():
    df_dataset_up = pd.read_csv(f'simple_reg_{config.RUNDATE}/df_dataset_up.csv', index_col=0, encoding='shift-jis')
    target_code_list = df_dataset_up['コード'].tolist()
    print(df_dataset_up)

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

    # 結果
    df_result = pd.DataFrame({
        'コード':code_list,
        'buy':buy_list,
        'sale':sale_list,
        'benefit':benefit_list,
        'benefit_ratio':benefit_ratio_list
    })
    # df_result['コード'] = df_result['コード'].astype(str)
    df_simulate = pd.merge(df_dataset_up, df_result, on='コード', how='left')
    df_simulate.to_csv(f'simple_reg_{config.RUNDATE}/df_simulate.csv', encoding='shift-jis')


def main():
    simulate()


if __name__ == '__main__':
    main()
