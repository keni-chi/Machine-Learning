import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RANSACRegressor


# データ読み込み
boston = load_boston()
X_np = boston.data
y_np = boston.target
columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 
           'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
           'TAX', 'PTRATIO', 'B', 'LSTAT']
df_X = pd.DataFrame(data=X_np, columns=columns, dtype='float')
df_y = pd.DataFrame(data=y_np, columns=['MEDV'], dtype='float')
X = df_X[['RM']].values
y = df_y['MEDV'].values

# RANSAC
ransac = RANSACRegressor(LinearRegression(), 
                         max_trials=100, 
                         min_samples=50, 
                         loss='absolute_loss', 
                         residual_threshold=5.0, 
                         random_state=0)


ransac.fit(X, y)

# print('正常値の取り出し')
# print(ransac.inlier_mask_)
inlier_mask = ransac.inlier_mask_  # 正常値の取り出し
outlier_mask = np.logical_not(inlier_mask)

line_X = np.arange(3, 10, 1)
print(line_X)
# line_X = np.arange(X.min(), X.max())
# print(line_X)

line_y_ransac = ransac.predict(line_X[:, np.newaxis])
print(line_y_ransac.shape)
print(line_y_ransac)

plt.scatter(X[inlier_mask], y[inlier_mask],
            c='steelblue', edgecolor='white', 
            marker='o', label='Inliers')
plt.scatter(X[outlier_mask], y[outlier_mask],
            c='limegreen', edgecolor='white', 
            marker='s', label='Outliers')
plt.plot(line_X, line_y_ransac, color='black', lw=2)   
plt.xlabel('Average number of rooms [RM]')
plt.ylabel('Price in $1000s [MEDV]')
plt.legend(loc='upper left')

plt.show()

