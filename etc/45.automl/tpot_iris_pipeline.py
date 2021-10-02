import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline, make_union
from sklearn.tree import DecisionTreeClassifier
from tpot.builtins import StackingEstimator
from sklearn.datasets import load_iris


# NOTE: Make sure that the outcome column is labeled 'target' in the data file
# tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
iris = load_iris()
df_X = pd.DataFrame(iris.data, columns=iris.feature_names)
df_y = pd.DataFrame(iris.target, columns=['target'])

# features = tpot_data.drop('target', axis=1)
features = df_X


training_features, testing_features, training_target, testing_target = \
            train_test_split(features, df_y['target'], random_state=None)

# Average CV score on the training set was: 1.0
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=MultinomialNB(alpha=0.1, fit_prior=False)),
    DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_leaf=12, min_samples_split=14)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
print(len(results))  ## 150/4=37.5
print(results)
