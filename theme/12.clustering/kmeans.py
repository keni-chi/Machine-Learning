import matplotlib.pyplot as plt
from sklearn import cluster
from sklearn import datasets

# iris データセットをロード
iris = datasets.load_iris()
data = iris['data']

# 色を分けて可視化する場合
features = iris.data[:, [0, 2]]
plt.scatter(*features.T, c=[['orange', 'green', 'blue'][x] for x in iris.target])
plt.show()

# k-means モデルの作成
model = cluster.KMeans(n_clusters=3)
model.fit(data)
labels = model.labels_
print(type(labels))

# 処理後に可視化する場合
fig = plt.figure()
features = data[:, [0, 2]]
plt.scatter(*features.T, c=[['orange', 'green', 'blue'][x] for x in labels])
plt.show()
