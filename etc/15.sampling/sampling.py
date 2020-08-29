import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE, SMOTENC


# iris データセットをロード
iris = datasets.load_iris()

X = iris['data']
X = X[80:]
y = iris['target']
y = y[80:]


print('A001')
print(X.shape)
print(y.shape)


# print('A002')
# sm = SMOTE(kind='svm')
# X_res, y_res = sm.fit_sample(X, y)
# print(X_res.shape)
# print(y_res.shape)


print('A003: デフォルトで利用')
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_sample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)
print(X_res[-1])


print('A004: k近傍の数を変更してみる')
sm = SMOTE(sampling_strategy='auto', k_neighbors=1, n_jobs=1, random_state=42)
X_res, y_res = sm.fit_resample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)
print(X_res[-1])


print('A005: サンプリング数の調整')
sm = SMOTE(sampling_strategy=0.9, random_state=42)
X_res, y_res = sm.fit_resample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)
print(X_res[-1])


print('A006: SMOTENCを試してみる。')
sm = SMOTENC(categorical_features = [3], sampling_strategy='auto', random_state=42)  # カテゴリ値の位置（列番号）
X_res, y_res = sm.fit_resample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)
print(X_res[-1])
