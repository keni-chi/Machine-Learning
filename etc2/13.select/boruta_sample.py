import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import cluster
from sklearn import datasets
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# iris データセットをロード
iris = datasets.load_iris()

x = iris['data']
# x = np.insert(x, 4, 100, axis=1)   # Rejectedを試す
# print(x)   # Rejectedを試す
y = iris['target']

# 学習データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

rf = RandomForestClassifier(n_estimators=20,n_jobs=-1)
feat_selector = BorutaPy(rf, n_estimators='auto', two_step=False,verbose=2, random_state=42)
feat_selector.fit(X_train,y_train)

# SepalLength	SepalWidth	PetalLength	PetalWidth	Name
# 「試行回数」、「重要と見做した特徴量の数」、「判断に悩んでいる特徴量の数」、「重要でないと判断した特徴量の数」
# Iteration: 	8 / 100
# Confirmed: 	4
# Tentative: 	0
# Rejected: 	1
print('feat_selector----')
print(feat_selector)
print('feat_selector.support_----')
print(feat_selector.support_)

print('特徴選択----')
df = pd.DataFrame(iris.data)
# df['A'] = 100   # Rejectedを試す
print(df.head())

X_train_selected = df.iloc[:,feat_selector.support_]
print(X_train_selected.head())
