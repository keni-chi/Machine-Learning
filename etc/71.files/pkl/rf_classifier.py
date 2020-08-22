import numpy as np
import matplotlib.pyplot as plt
import pickle
import sklearn.datasets as datasets
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def plot_pred_and_actual(y_pred, y_actual):
    fig = plt.figure(figsize=(14,7))
    ax = fig.add_subplot(111)
    ax.scatter(2,2,color="white")
    ax.plot(y_pred,lw=1,color="red",label="y_pred")
    ax.plot(y_actual,lw=1,color="blue",label="y_actual")
    ax.legend()
    plt.show()


# irisデータの読み込み
iris = datasets.load_iris()
X = iris['data']
y = iris.target

# 学習データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# ランダムフォレストのモデル構築
model = RandomForestClassifier(n_estimators=20,n_jobs=-1)
model.fit(X_train, y_train)

#モデルを保存する
print('モデルを保存-------------------start')
filename = 'model.pkl'
pickle.dump(model, open(filename, 'wb'))

#モデルを読み込む
print('モデルを読み込む-------------------start')
m = pickle.load(open(filename, 'rb'))

#正解率
print ("train正解率",m.score(X_train, y_train))
print ("test正解率",m.score(X_test, y_test))

#予測データ作成
y_train_pred = m.predict(X_train)
y_test_pred = m.predict(X_test)

# # 予測と正解の比較
# plot_pred_and_actual(y_train, y_train_pred)
# plot_pred_and_actual(y_test, y_test_pred)
