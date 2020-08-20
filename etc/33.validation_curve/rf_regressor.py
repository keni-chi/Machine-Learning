import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import validation_curve


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


def plot_rf_feature_importance(feature, columns):
    # 特徴量の重要度順（降順）
    indices = np.argsort(feature)[::-1]

    plt.title('Feature Importance')
    plt.bar(range(len(feature)),feature[indices], color='lightblue', align='center')
    plt.xticks(range(len(feature)), columns[indices], rotation=90)
    plt.xlim([-1, len(feature)])
    plt.tight_layout()
    plt.show()


# データ読み込み
boston = load_boston()
X_array = boston.data
y_array = boston.target
X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.2, random_state=0)


print('デフォルト--------------start')
# 学習
model = RandomForestRegressor(random_state=0)
model.fit(X_train, y_train)

# 評価
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
plot_regressor(y_train_pred, y_train)

y_test_pred = model.predict(X_test)
plot_regressor(y_test_pred, y_test)


#特徴量の重要度
feature = model.feature_importances_
# df = pd.DataFrame(boston.data, columns=boston.feature_names)
columns = boston.feature_names[0:]
plot_rf_feature_importance(feature, columns)
print('デフォルト--------------end')


# validation_curve
n_estimators = [10, 20, 30, 40, 50]
train_scores, test_scores = validation_curve(RandomForestRegressor(), X_array, y_array, param_name="n_estimators",
                                             param_range=n_estimators, cv=10)
plt.plot(n_estimators, train_scores.mean(axis=1), label="train score")
plt.plot(n_estimators, test_scores.mean(axis=1), label="test score")
plt.legend(loc="best")
plt.show()
