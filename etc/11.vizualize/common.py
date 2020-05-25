import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# 色を分けて可視化する場合
iris = load_iris()
features = iris.data[:, [0, 2]]
plt.scatter(*features.T, c=[['orange', 'green', 'blue'][x] for x in iris.target])
plt.show()

# データセット読み込み
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
x = iris.data
y = iris.target

# 学習データとテストデータに分割
print(type(x))
print(type(y))
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
print(type(x_train))
print(type(x_test))

# ランダムフォレストのモデル構築
# n_jobs : 全てのコアを使用(-1)
# n_estimators : 使用する決定木数(デフォルト10)
model = RandomForestClassifier(n_estimators=20,n_jobs=-1)
model.fit(x_train, y_train)

#正解率
print ("train正解率",model.score(x_train,y_train))
print ("test正解率",model.score(x_test,y_test))

#予測データ作成
y_pre = model.predict(x_train)

# 予測と正解の比較
fig = plt.figure(figsize=(14,7))
ax = fig.add_subplot(111)
ax.scatter(2,2,color="white")
ax.plot(y_train,lw=1,color="red",label="train")
ax.plot(y_pre,lw=1,color="blue",label="predict")
ax.legend()
plt.show()
