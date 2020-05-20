# 64次元の特徴量を持つデータを2次元の散布図としてプロット
from sklearn import random_projection
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

digits = datasets.load_digits()
print(type(digits.data))
print(digits.data.shape)
print(digits.data)
print(digits.target)

X_TSNEprojected = TSNE(n_components=2, random_state=0).fit_transform(digits.data)
X_Gprojected    = random_projection.GaussianRandomProjection(n_components=2).fit_transform(digits.data)
X_Sprojected    = random_projection.SparseRandomProjection(n_components=2).fit_transform(digits.data)

plt.scatter(X_TSNEprojected[:,0], X_TSNEprojected[:,1], c=digits.target,alpha=0.5, cmap='rainbow')
plt.colorbar()
plt.show()
plt.scatter(X_Gprojected[:, 0], X_Gprojected[:, 1], c=digits.target, cmap='rainbow')
plt.colorbar()
plt.show()
plt.scatter(X_Sprojected[:, 0], X_Sprojected[:, 1], c=digits.target, cmap='rainbow')
plt.colorbar()
plt.show()

