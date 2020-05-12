import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def plot_regressor(pred, actual):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    ax.scatter(pred,actual)
    ax.set_title('pred vs actual')
    ax.set_xlabel('pred')
    ax.set_ylabel('actual')
    lims = [0, 60]
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    plt.grid()
    plt.show()

# データ読み込み
boston = load_boston()
X_array = boston.data
y_array = boston.target
X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.2, random_state=0)

# 学習
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 評価
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
plot_regressor(y_train_pred, y_train)

y_test_pred = model.predict(X_test)
plot_regressor(y_test_pred, y_test)
