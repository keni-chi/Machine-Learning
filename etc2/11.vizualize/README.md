# vizualize

グラフ
    統計量のグラフ
    seabornでペアプロット図

多次元空間⇔２次元平面
    多次元空間において近いところにあるサンプル同士は、２次元平面においても近いか。
        主成分分析(Principal Component Analysis, PCA)
        Kernel PCA
        Factor Analysis (FA)
        Multi-Dimensional Scaling (MDS)
        Isometric feature mapping (Isomap)
    上記を満たさない
        自己組織化マップ (Self-Organizing Map, SOM) 
        t-distributed Stochastic Neighbor Embedding (tSNE) 
    各手法の概要
        主成分分析 (Principal Component Analysis, PCA) 
            見える化 (可視化) する手法
            多変量 (多次元) のデータセットを低次元化する方法
            データセットのもつ情報量をなるべく失わないように元の次元からより低い次元でデータセットを表現
            説明変数 X から互いに無相関な成分 (主成分) を計算する手法
            主成分は、寄与率の大きい順に並べることが可能
        Independent Component Analysis, ICA
            説明変数 X から互いに独立な成分 (独立成分) を計算する手法
            独立成分は、どれも平等
            独立は無相関より強力
            データセット内に外れ値があると、外れ値が強調されたような独立成分が抽出される
        自己組織化マップ(Self-Organizing Map, SOM)
            ニューラルネットワークの１つ
            データを可視化・見える化するための非線形手法
            主成分分析などとは異なり、はじめに二次元平面の座標を作ってしまい、それを実際の多次元空間のサンプルに合わせ込む
            オーバーフィッティングを起こしやすいので注意が必要
            SOMのいろいろな問題点を解決した、上位互換の手法にGenerative Topographic Mapping (GTM) がある
            GTMに対するSOMのメリットは、手法の説明が簡単、コーディングがしやすい
        t-distributed Stochastic Neighbor Embedding (t-SNE) ～データの可視化に特化した手法～
            非線形の可視化手法の一つ
            PCA や GTM のように、元の空間から低次元空間 (基本的には二次元平面) に写像させる関数が得られるわけではないので注意
            写像というよりは、サンプル全体が見やすいように二次元平面に配置するイメージ
            可視化に特化した手法
            元の空間におけるサンプル間の距離関係が二次元平面におけるサンプル間の距離関係として保持されるほど値が小さくなる目的関数を準備して、それが小さくなるように二次元平面にサンプルを配置させる



# 参考
[データ解析に関するいろいろな手法・考え方・注意点のまとめ](https://datachemeng.com/summarydataanalysis/)  
[pythonで主成分分析(PCA)と独立成分分析(ICA)](https://qiita.com/yuta-takahashi/items/c05908db9aebd1afa99f)  
[Pythonで主成分分析（PCA）を行う方法を現役エンジニアが解説【初心者向け】](https://techacademy.jp/magazine/22717)  
[自己組織化マップ](http://www.gaya.jp/spiking_neuron/som.htm)  
[tSNEでMNISTを軽やかに鮮やかにマッピングしていく](https://qiita.com/szk1akhr/items/55db2aa792efcebeeb7e)  
