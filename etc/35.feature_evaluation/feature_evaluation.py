# pip install shap==0.29.3
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.DataFrame(iris.target, columns=['y'])

# 学習データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


print('-------------------------------------')
# ランダムフォレストのモデル構築
model = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
        max_depth=25, max_features='auto', max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_impurity_split=None,
        min_samples_leaf=1, min_samples_split=15,
        min_weight_fraction_leaf=0.0, n_estimators=50, n_jobs=4,
        oob_score=False, random_state=0, verbose=0, warm_start=False)
model.fit(X_train, y_train)

print(type(X_train))

# load JS visualization code to notebook
shap.initjs()

# Create object that can calculate shap values
explainer = shap.TreeExplainer(model)
# Calculate SHAP values
shap_values = explainer.shap_values(X_train)
# visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
shap.force_plot(explainer.expected_value[0], shap_values[0][0], X_train.iloc[0,:])



print('-------------------------------------')
#RandamForestの学習済みモデルを用意する。
model = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
        max_depth=25, max_features='auto', max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_impurity_split=None,
        min_samples_leaf=1, min_samples_split=15,
        min_weight_fraction_leaf=0.0, n_estimators=50, n_jobs=4,
        oob_score=False, random_state=0, verbose=0, warm_start=False)
model.fit(X_train, y_train)
 
#SHAPのExplainerを用意する。ランダムフォレストなのでTreeExplainerを使う。
explainer = shap.TreeExplainer(model)
 
#irisの最初のデータを例にshap_valuesを求める。
shap_values = explainer.shap_values(X_train.loc[[0]])
 
#予測に使ったデータに対してsetosaとなる確率とその要因について可視化する。
shap.force_plot(explainer.expected_value[0], 
                shap_values[0], 
                X_train.loc[[0]], 
                matplotlib=True,
                )

