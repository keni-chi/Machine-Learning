from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import glob
import datetime as dt
import seaborn as sns
import openpyxl

sub_folder = 'processed'

def corr_stock_usjp(df_stock, df_usjp):
    df_dataset = pd.merge(df_stock, df_usjp, on='Date', how='left')
    df_dataset = df_dataset.set_index('Date')

    df_corr = df_dataset.corr().reset_index().sort_values('usjp')[['index', 'usjp']].rename(columns={'index': 'コード'})
    # df_corr = df_corr[(df_corr['usjp']>=0.8)|(df_corr['usjp']<=-0.8)]
    df_corr = df_corr[df_corr['usjp']<=-0.5]
    df_corr = df_corr[df_corr['usjp']!=1.0]

    # コードマスタに相関係数を結合
    df_code = pd.read_csv('./data_j_prime.csv', encoding='shift_jis')
    df_corr['コード'] = df_corr['コード'].astype('int')
    df_code_corr = pd.merge(df_code, df_corr, on='コード', how='left')
    df_code_corr.to_csv(f'{sub_folder}/df_code_corr.csv', encoding='shift_jis')

    # 散布図
    print('--')
    for c in df_corr['コード'].tolist():
        code = str(c)
        print(code)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(df_dataset[code], df_dataset['usjp'])
        ax.set_title(code)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)
        plt.savefig(f'{sub_folder}/png/{code}.png')
        plt.close()


def corr_index(df_usjp, df_dow, df_nikkei, df_oil):
    pass
    # dow
    df_dow['取引日'] = df_dow['取引日'].astype('str')
    df_dow['取引日'] =  df_dow['取引日'].str[:4] + '-' + df_dow['取引日'].str[4:6] + '-' + df_dow['取引日'].str[6:8]
    df_dow = df_dow.rename(columns={'取引日': 'Date', '終値': 'dow'})
    df_dow = df_dow[['Date', 'dow']]
    print('aa')
    print(df_dow)

    # nikkei
    print(df_nikkei.columns)
    df_nikkei = df_nikkei.rename(columns={'date': 'Date', ' value': 'nikkei'})
    print(df_nikkei)
    df_nikkei = df_nikkei[['Date', 'nikkei']]
    print('bb')
    print(df_nikkei)

    # oil
    df_oil['date'] = df_oil['date'].replace('年', '-', regex=True)
    df_oil['date'] = df_oil['date'].replace('月', '-', regex=True)
    df_oil['date'] = df_oil['date'].replace('日', '', regex=True)
    df_oil['y'] = df_oil['date'].str.split(pat='-', expand=True)[0]
    df_oil['m'] = df_oil['date'].str.split(pat='-', expand=True)[1]
    df_oil['d'] = df_oil['date'].str.split(pat='-', expand=True)[2].replace(' ', '', regex=True)
    df_oil['m'] = df_oil['m'].str.zfill(2)
    df_oil['d'] = df_oil['d'].str.zfill(2)
    df_oil['Date'] = df_oil['y'] + '-' + df_oil['m'] + '-' + df_oil['d']
    df_oil = df_oil.rename(columns={'WTI原油     ': 'oil'})
    df_oil = df_oil[['Date', 'oil']]
    print('c1')
    print(df_oil)

    # 結合
    df_corr_index = pd.merge(df_usjp, df_dow, on='Date', how='inner')
    print('DD1')
    print(df_corr_index)
    df_corr_index = pd.merge(df_corr_index, df_nikkei, on='Date', how='inner')
    print('DD2')
    print(df_corr_index)
    df_corr_index = pd.merge(df_corr_index, df_oil, on='Date', how='inner')
    print('DD3')
    print(df_corr_index)

    # ペアプロット
    pg = sns.pairplot(df_corr_index)
    plt.tight_layout()
    pg.savefig(f'{sub_folder}/png/df_corr_index.png')


def to_index_day():
    print('データ読み込み-------')
    # df_stock = pd.read_csv('./processed/df_test2.csv', encoding='shift_jis', index_col=0)
    df_usjp = pd.read_csv('./index/usdjpy_d/usdjpy_d.csv', encoding='shift_jis').rename(columns={'Close': 'usjp'})[['Date', 'usjp']]
    df_dow = pd.read_csv('./index/index/K_dji_jpy.csv', encoding='shift_jis', header=1)
    df_nikkei = pd.read_csv('./index/index/nikkei-225-index-historical-chart-data.csv', encoding='shift_jis', skiprows=15)
    df_oil = pd.read_excel('./index/oil/HistoricalPrices.xls', header=3, index_col=1)[:-2].drop('Unnamed: 0', axis=1).reset_index().rename(columns={'index': 'date'})
    # df_oil.to_csv('test.csv')
    print(df_usjp)
    print(df_dow)
    print(df_nikkei)
    print(df_oil)

    # 株と円相場の相関
    # corr_stock_usjp(df_stock, df_usjp)

    # 指標間の相関
    corr_index(df_usjp, df_dow, df_nikkei, df_oil)



def main():
    to_index_day()


if __name__ == '__main__':
    main()
