from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import os


def fit_predict(df):
    df_none_index = df.reset_index(drop=True)
    df = df.reset_index().reset_index()
    code_list, a_list, b_list, R2_list = [], [], [], []
    for code in df_none_index.columns.tolist():
        X = df[['level_0']]
        y = df[code]
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a = model_lr.coef_
        b = model_lr.intercept_
        R2 = model_lr.score(X, y)
        code_list.append(code)
        a_list.append(a[0])
        b_list.append(b)
        R2_list.append(R2)
    df_result = pd.DataFrame({
        'code':code_list,
        'a':a_list,
        'b':b_list,
        'R2':R2_list
    })

    # コード情報の結合
    df_result = df_result.rename({'code': 'コード'}, axis=1)
    df_ext = pd.read_csv('./dataset/data_j_extract.csv', encoding='shift_jis')
    df_result = pd.merge(df_ext, df_result, on='コード', how='inner')

    # 出力
    df_result = df_result.sort_values(by=['a'], ascending=False)
    df_result.to_csv('lr/df_result.csv', encoding='shift-jis')


def main():
    df = pd.read_csv('./dataset/dataset.csv',index_col=0)
    df = df.dropna().T
    print(df)
    print(df.info())
    fit_predict(df)


if __name__ == '__main__':
    main()
