import numpy as np
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
from sklearn.decomposition import FastICA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# irisデータの読み込み
iris = datasets.load_iris()
data = iris['data']
print(data.shape)

# 散布図に描画
fig = plt.figure()
plt.plot(data[:,2], data[:,3], 'k.')
plt.xlabel("petalLength")
plt.ylabel("petalWidth")
plt.show()

#ICAの実行
ICA = FastICA(n_components=2, random_state=0)#20個の基底（コンポネント）を作る
X_transformed = ICA.fit_transform(data)

# 色を分けて可視化する場合
features = iris.data[:, [0, 2]]
plt.scatter(*features.T, c=[['orange', 'green', 'blue'][x] for x in iris.target])
plt.show()

# 処理後に可視化する場合
fig = plt.figure()
features = X_transformed[:, [0, 1]]
plt.scatter(*features.T, c=[['orange', 'green', 'blue'][x] for x in iris.target])
plt.show()
print('--------------------------------')

# x
ICA = FastICA(n_components=3, random_state=0)#20個の基底（コンポネント）を作る
x = ICA.fit_transform(data)
print(x)

# y
y = iris.target

# 学習データとテストデータに分割
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# ランダムフォレストのモデル構築
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
