# ライブラリーのインポート
import os
import pandas as pd
import numpy as np
# from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import optuna
from optuna.samplers import TPESampler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import Ridge
import catboost as cb
from catboost import CatBoost, Pool


# データセットの読込み
housing = fetch_california_housing()
# 説明変数の格納
df = pd.DataFrame(housing.data, columns = housing.feature_names)
# 目的変数の追加
df['MEDV'] = housing.target
# データの中身を確認
print(df.head())

# ランダムシード値
RANDOM_STATE = 10
# 学習データと評価データの割合
TEST_SIZE = 0.2
# 学習データと評価データを作成
x_train, x_test, y_train, y_test = train_test_split(
    df.iloc[:, 0 : df.shape[1] - 1],
    df.iloc[:, df.shape[1] - 1],
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
)
# trainのデータセットの2割をモデル学習時のバリデーションデータとして利用する
x_train, x_valid, y_train, y_valid = train_test_split(
    x_train, y_train, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
print(x_train.head())
print(y_valid)
y_train = pd.DataFrame({'MEDV': y_train})
y_valid = pd.DataFrame({'MEDV': y_valid})

 # 初期化
scaler = StandardScaler()
 # データに合わせて計算しスケーリングする
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_valid = scaler.transform(x_valid)

y_scaler = StandardScaler()
y_scaler.fit(y_train)
y_train = y_scaler.transform(y_train)
y_valid = y_scaler.transform(y_valid)
print(y_valid)


def objective(trial):
    param_alpha = trial.suggest_loguniform("alpha", 0.0001, 100.0)
    model = Ridge(alpha=param_alpha, random_state=0)
    model.fit(
        x_train,
        y_train
    )
    preds = model.predict(x_valid)
    # mae = mean_absolute_error(y_valid, preds)
    val_mape = np.mean(np.abs((preds-y_valid)/y_valid))*100
    return val_mape


# optunaで最適値を見つける
# create_studyメソッドの引数"sampler"にサンプラーと乱数シードを指定
study = optuna.create_study(direction='minimize', sampler=TPESampler(seed=RANDOM_STATE))
study.optimize(objective, n_trials=3)


# 最適パラメータの表示と保持
best_params = study.best_trial.params
best_score = study.best_trial.value
print(f'最適パラメータ {best_params}\nスコア {best_score}')


# チューニングしたハイパーパラメーターをフィット
optimised_model = Ridge(alpha=best_params['alpha'], random_state=0)
optimised_model.fit(x_train, y_train)
y_pred = optimised_model.predict(x_valid)



############################################
def cb_objective(trial):
    param = {
        "iterations": trial.suggest_int("iterations", 50, 300),
        "depth": trial.suggest_int("depth", 4, 10),
        "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.3),
        "random_strength": trial.suggest_int("random_strength", 0, 100),
        "bagging_temperature": trial.suggest_loguniform(
            "bagging_temperature", 0.01, 100.00
        ),
        "od_type": trial.suggest_categorical("od_type", ["IncToDec", "Iter"]),
        "od_wait": trial.suggest_int("od_wait", 10, 50),
    }
    model = cb.CatBoostRegressor(**param, random_state=0)
    model.fit(
        x_train,
        y_train,
        eval_set=[(x_valid, y_valid)],
        early_stopping_rounds=100,
        verbose=False,
    )
    preds = model.predict(x_valid)
    val_mape = np.mean(np.abs((preds-y_valid)/y_valid))*100
    return val_mape

# optunaで最適値を見つける
# create_studyメソッドの引数"sampler"にサンプラーと乱数シードを指定
study = optuna.create_study(direction='minimize', sampler=TPESampler(seed=RANDOM_STATE))
study.optimize(cb_objective, n_trials=50)

# 最適パラメータの表示と保持
best_params = study.best_trial.params
best_score = study.best_trial.value
print(f'最適パラメータ {best_params}\nスコア {best_score}')

# チューニングしたハイパーパラメーターをフィット
optimised_model = cb.CatBoostRegressor(**(best_params))
optimised_model.fit(x_train, y_train)
y_pred = optimised_model.predict(x_valid)

