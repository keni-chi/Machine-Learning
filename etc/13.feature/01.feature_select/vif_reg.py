import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


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
df_X = pd.DataFrame(data=boston.data, columns=boston.feature_names, dtype='float')
df_y = pd.DataFrame(data=boston.target, columns=['MEDV'], dtype='float')
df_Xy = pd.concat([df_X, df_y], axis=1)

# vifを計算する-------------------------------
vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(df_X.values, i) for i in range(df_X.shape[1])]
vif = vif.set_index(boston.feature_names)
print(vif)

#vifをグラフ化する:  VIF>10の場合は多重共線性が強い
plt.plot(vif["VIF Factor"])
# plt.grid() 
# plt.show()
df_X = df_X[['CRIM', 'ZN', 'CHAS', 'LSTAT', 'ZN', 'INDUS', 'DIS', 'RAD']]

# split-----------------------------
X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.2, random_state=0)
y_train = y_train['MEDV']
y_test = y_test['MEDV']

# 標準化処理
sc = StandardScaler()
sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)

# 学習
model = RandomForestRegressor(random_state=0)
# model = Lasso()
model.fit(X_train, y_train)

# 評価(R^2)
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# MAE計算
mae = mean_absolute_error(y_test, y_test_pred)
print('MAE : {:.3f}'.format(mae))

# RMSE計算
rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
print('RMSE : {:.3f}'.format(rmse))
