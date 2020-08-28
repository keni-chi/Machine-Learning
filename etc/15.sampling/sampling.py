import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE


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


print('A003')
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_sample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)


print('A004')
sm = SMOTE(sampling_strategy='auto', k_neighbors=1, n_jobs=1, random_state=42)
X_res, y_res = sm.fit_resample(X, y)
print(X_res.shape)
print(y_res.shape)
print(y_res)

