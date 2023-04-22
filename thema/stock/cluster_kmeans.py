from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from matplotlib import cm
from sklearn.datasets import make_blobs  # ダミーデータの生成用
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler


# # サンプルデータ
# # Xには1つのプロットの(x,y)が、yにはそのプロットの所属するクラスター番号が入る
# X,y=make_blobs(n_samples=150,         # サンプル点の総数
#                n_features=2,          # 特徴量（次元数）の指定  default:2 
#                centers=3,             # クラスタの個数
#                cluster_std=0.5,       # クラスタ内の標準偏差 
#                shuffle=True,          # サンプルをシャッフル
#                random_state=0)        # 乱数生成器の状態を指定
# print(X)
# print(y)


df = pd.read_csv('./dataset/dataset.csv',index_col=0)
X = df.dropna()
print(X)
print(X.info())

# 標準化
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
print('X_std')
print(X_std)

def search_kmeans():
    for n_cluster in range(3,31):
        print(n_cluster)

        # 構築
        km = KMeans(n_clusters=n_cluster,    # クラスターの個数
                    init='k-means++',        # セントロイドの初期値をランダムに設定
                    n_init=10,               # 異なるセントロイドの初期値を用いたk-meansあるゴリmズムの実行回数
                    max_iter=300,            # k-meansアルゴリズムの内部の最大イテレーション回数
                    tol=1e-04,               # 収束と判定するための相対的な許容誤差
                    random_state=0)          # セントロイドの初期化に用いる乱数発生器の状態
        y_km = km.fit_predict(X_std)

        # 評価
        cluster_labels = np.unique(y_km)       # y_kmの要素の中で重複を無くす
        n_clusters=cluster_labels.shape[0]     # 配列の長さを返す。つまりここでは n_clustersで指定した3となる
        # シルエット係数を計算
        silhouette_vals = silhouette_samples(X_std,y_km,metric='euclidean')  # サンプルデータ, クラスター番号、ユークリッド距離でシルエット係数計算
        y_ax_lower, y_ax_upper= 0,0
        yticks = []

        for i,c in enumerate(cluster_labels):
                c_silhouette_vals = silhouette_vals[y_km==c]      # cluster_labelsには 0,1,2が入っている（enumerateなのでiにも0,1,2が入ってる（たまたま））
                c_silhouette_vals.sort()
                y_ax_upper += len(c_silhouette_vals)              # サンプルの個数をクラスターごとに足し上げてy軸の最大値を決定
                color = cm.jet(float(i)/n_clusters)               # 色の値を作る
                plt.barh(range(y_ax_lower,y_ax_upper),            # 水平の棒グラフのを描画（底辺の範囲を指定）
                                c_silhouette_vals,               # 棒の幅（1サンプルを表す）
                                height=1.0,                      # 棒の高さ
                                edgecolor='none',                # 棒の端の色
                                color=color)                     # 棒の色
                yticks.append((y_ax_lower+y_ax_upper)/2)          # クラスタラベルの表示位置を追加
                y_ax_lower += len(c_silhouette_vals)              # 底辺の値に棒の幅を追加

        silhouette_avg = np.mean(silhouette_vals)                 # シルエット係数の平均値
        plt.axvline(silhouette_avg,color="red",linestyle="--")    # 係数の平均値に破線を引く 
        plt.yticks(yticks,cluster_labels + 1)                     # クラスタレベルを表示
        plt.ylabel('Cluster')
        plt.xlabel('silhouette coefficient')
        # plt.show()
        plt.savefig(f'kmeans/eva/c_{str(n_cluster)}.png')
        plt.close() 


# 探索時
search_kmeans()

# 構築
km = KMeans(n_clusters=30,    # クラスターの個数
            init='k-means++',        # セントロイドの初期値をランダムに設定
            n_init=10,               # 異なるセントロイドの初期値を用いたk-meansあるゴリmズムの実行回数
            max_iter=300,            # k-meansアルゴリズムの内部の最大イテレーション回数
            tol=1e-04,               # 収束と判定するための相対的な許容誤差
            random_state=0)          # セントロイドの初期化に用いる乱数発生器の状態
y_km = km.fit_predict(X_std)

# codeとクラスタの対応
df_map = X.copy()
df_map['class'] = y_km
df_map = df_map[['class']]
print(df_map)


# グラフ描画
df_plt = X.T
print(df_plt)
for n_cluster in range(30):
    print(n_cluster)
    df_target = df_map[df_map['class'] == n_cluster]
    code_list = df_target.index.tolist()
    print(code_list)

    # クラスタ毎に絞り込み
    df_clster_n = df_plt[code_list]
    print('A01')
    print(df_clster_n)


    df_clster_n.plot()
    plt.savefig(f'kmeans/trend/trend_{str(n_cluster)}.png')
    plt.close('all')


    # # グラフ描画
    # fig, ax = plt.subplots()
    # plt.xticks(rotation=90)
    # ax.plot(df.index, df['value01'], color='b')

    # # X軸を共有する双軸
    # ax2 = ax.twinx()

    # ax2.plot(df.index, df['value02'], color='r')
    # plt.show()