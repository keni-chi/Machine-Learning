import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


def iris_df():
    # scikit-learnのirisデータセット読み込み
    iris = load_iris()
    # irisデータセットをPandasのDetaFrameに変換
    df = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])
 
    # 正規化
    items = df.columns
    index = df.index
    df = pd.DataFrame(MinMaxScaler().fit_transform(df))
    df.columns = items #カラム名を再設定
    df.index = index # インデックス名を再設定
     
    return df


df = iris_df()
# ウォード法, ユーグリッド距離
Z = linkage(pdist(df[df.columns[2:4]].as_matrix(), metric='euclidean'), method='ward')
#metric = 'braycurtis', 
#metric = 'canberra', 
#metric = 'chebyshev', 
#metric = 'cityblock', 
#metric = 'correlation', 
#metric = 'cosine', 
#metric = 'euclidean', 
#metric = 'hamming', 
#metric = 'jaccard', 
#method= 'single')
#method = 'average')
#method= 'complete')
#method='weighted')

plt.figure(figsize=(14, 5))
plt.ylabel('Distance')
dendrogram(Z, leaf_rotation=90., leaf_font_size=8., labels=df['target'].tolist())
print(len(df.index.values))
print(len(df['target'].tolist()))
# print(df['target'])

plt.show()
