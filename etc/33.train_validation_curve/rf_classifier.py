import numpy as np
import matplotlib.pyplot as plt
import pickle
import sklearn.datasets as datasets
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import validation_curve


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

# validation_curve
n_estimators = [10, 20, 30, 40, 50]
train_scores, test_scores = validation_curve(RandomForestClassifier(), X, y, param_name="n_estimators",
                                             param_range=n_estimators, cv=10)
plt.plot(n_estimators, train_scores.mean(axis=1), label="train score")
plt.plot(n_estimators, test_scores.mean(axis=1), label="test score")
plt.legend(loc="best")
plt.show()
