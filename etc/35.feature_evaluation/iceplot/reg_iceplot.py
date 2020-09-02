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
X_array = pd.DataFrame(boston.data, columns=boston.feature_names)
y_array = boston.target
X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.2, random_state=0)


print('デフォルト--------------start')
# 学習
model = RandomForestRegressor(random_state=0)
model.fit(X_train, y_train)

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


print('PDP Isolate Plot--------------start')
# LSTAT（低所得者割合）の上昇は、住宅価格が低下する方向に寄与していることが分かる
from pdpbox import pdp, get_dataset, info_plots
# fig = plt.figure(figsize=(14,5))
pdp_goals = pdp.pdp_isolate(model=model, dataset=X_train, model_features=X_test.columns, feature='LSTAT')
pdp.pdp_plot(pdp_goals,'LSTAT')
plt.show()

pdp_goals = pdp.pdp_isolate(model=model, dataset=X_train, model_features=X_test.columns, feature='RM')
pdp.pdp_plot(pdp_goals,'RM')
plt.show()


print('PDP Interact Plot--------------start')
pdp_score = pdp.pdp_interact(model=model, dataset=X_train, model_features=X_test.columns, features=['LSTAT','RM'])
pdp.pdp_interact_plot(pdp_score,['LSTAT',"RM"],plot_type='grid',x_quantile=True,ncols=2,plot_pdp=True)
plt.show()

