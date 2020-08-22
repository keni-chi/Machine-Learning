import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint as sp_randint
from skopt import BayesSearchCV


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


print('grid_search1--------------start')
start_time = time.time()

grid = {
    "n_estimators": [i for i in range(1, 21)],
    "max_depth": [i for i in range(1, 5)],
    "criterion": ["mse"],
    "random_state": [i for i in range(0, 11)]
}

model_grid = GridSearchCV(RandomForestRegressor(),
                     grid,
                     cv=5)  # k分割交差検証

model_grid.fit(X_train, y_train)

model = model_grid.best_estimator_
print("Best Model Parameter: ", model_grid.best_params_)

# 評価
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
# plot_regressor(y_train_pred, y_train)

y_test_pred = model.predict(X_test)
# plot_regressor(y_test_pred, y_test)

#特徴量の重要度
feature = model.feature_importances_
# df = pd.DataFrame(boston.data, columns=boston.feature_names)
columns = boston.feature_names[0:]
# plot_rf_feature_importance(feature, columns)

end_time = time.time() - start_time
print ("processing_time:{0}".format(end_time) + "[sec]")
print('grid_search1--------------end')


print('random_search--------------start')
start_time = time.time()

# param_dist = {
#     "n_estimators": [i for i in range(1, 21)],
#     "max_depth": [i for i in range(1, 5)],
#     "criterion": ["mse"],
#     "random_state": [i for i in range(0, 11)]
# }

param_dist = {
    "n_estimators": [50, 100, 200, 300, 400, 500],  # 木の数  デフォルト:100
    "max_features": [1, 3, 10],  # 最適な分割を探すときに検討すべき特徴量の数  デフォルト:auto
    "min_samples_split": [2, 3, 10],  # 内部ノードを分割するために必要なサンプルの最小数  デフォルト:2
    "min_samples_leaf": [1, 3, 10],  # リーフノードに存在するために必要なサンプルの最小数  デフォルト:1
    "bootstrap": [True, False],  # ツリーの構築時に使用されるサンプルのブートストラップのランダム性  デフォルト:True
    "max_depth": [i for i in range(1, 5)],  # ツリーの最大深度  デフォルト:None
    "criterion": ["mse"],  #   デフォルト: "mse"
    "random_state": [i for i in range(0, 5)]  #   デフォルト:None
}


model_random = RandomizedSearchCV(RandomForestRegressor(), param_distributions=param_dist, cv=5, n_iter=100)

model_random.fit(X_train, y_train)

model = model_random.best_estimator_
print("Best Model Parameter: ", model_random.best_params_)

# 評価
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
# plot_regressor(y_train_pred, y_train)

y_test_pred = model.predict(X_test)
# plot_regressor(y_test_pred, y_test)

end_time = time.time() - start_time
print ("processing_time:{0}".format(end_time) + "[sec]")
print('random_search--------------end')


print('bayes_search--------------start')
start_time = time.time()

param_dist = {
    "n_estimators": [50, 100, 200, 300, 400, 500],
    "max_features": [1, 3, 10],
    "min_samples_split": [2, 3, 10],
    "min_samples_leaf": [1, 3, 10],
    "bootstrap": [True, False],
    "max_depth": [i for i in range(1, 5)],
    "criterion": ["mse"],
    "random_state": [i for i in range(0, 5)]
}

search = BayesSearchCV(RandomForestRegressor(), param_dist, cv=5, n_iter=100)

model_random.fit(X_train, y_train)

model = model_random.best_estimator_
print("Best Model Parameter: ", model_random.best_params_)

# 評価
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# 予測
y_train_pred = model.predict(X_train)
# plot_regressor(y_train_pred, y_train)

y_test_pred = model.predict(X_test)
# plot_regressor(y_test_pred, y_test)

end_time = time.time() - start_time
print ("processing_time:{0}".format(end_time) + "[sec]")
print('bayes_search--------------end')


## 実行例
# 0.9762191609246614
# 0.7209305198692493

# Best Model Parameter:  {'criterion': 'mse', 'max_depth': 4, 'n_estimators': 20, 'random_state': 1}
# 0.9256577304121582
# 0.7399002566277912
# processing_time:313.2520363330841[sec]

# Best Model Parameter:  {'random_state': 0, 'n_estimators': 100, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 10, 'max_depth': 4, 'criterion': 'mse', 'bootstrap': True}
# 0.9270799469484265
# 0.7541943101433067
# processing_time:928.3689386844635[sec]

# Best Model Parameter:  {'random_state': 4, 'n_estimators': 200, 'min_samples_split': 3, 'min_samples_leaf': 3, 'max_features': 10, 'max_depth': 4, 'criterion': 'mse', 'bootstrap': True}
# 0.9164280817726044
# 0.680230289918484
# processing_time:75.13854193687439[sec]
