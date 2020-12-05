import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from boruta import BorutaPy
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


# データを読んでくる
boston = load_boston()
df_X = pd.DataFrame(boston.data, columns=boston.feature_names)
df_y = pd.Series(boston.target, name='target')
X_train, X_test, y_train, y_test = train_test_split(df_X, df_y, test_size=0.2, random_state=0)

# 全部の特徴量で学習
rf1 = RandomForestRegressor(n_jobs=-1, max_depth=5)
rf1.fit(X_train, y_train)
print('SCORE with ALL Features: %1.2f\n' % rf1.score(X_train, y_train))

# RandomForestRegressor
rf = RandomForestRegressor(n_jobs=-1, max_depth=5)
feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, max_iter=10, random_state=0)
feat_selector.fit(X_train.values, y_train.values)

# 選択された特徴量を確認
selected = feat_selector.support_
print('選択された特徴量の数: %d' % np.sum(selected))
print(selected)
print(X_train.columns[selected])

# 選択した特徴量で学習
X_train_selected = X_train[X_train.columns[selected]]
X_test_selected = X_test[X_test.columns[selected]]

rf2 = RandomForestRegressor(n_jobs=-1, max_depth=5)
rf2.fit(X_train_selected, y_train)
print('SCORE with selected Features: %1.2f' % rf2.score(X_train_selected, y_train))

# 予測
y_train_pred = rf2.predict(X_train_selected)
y_test_pred = rf2.predict(X_test_selected)

# MAE計算
mae = mean_absolute_error(y_test, y_test_pred)
print('MAE : {:.3f}'.format(mae))

# RMSE計算
rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
print('RMSE : {:.3f}'.format(rmse))
