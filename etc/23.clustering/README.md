# クラスタリング

手法
    階層的クラスタリング  

    k平均法 (k-means clustering) 非階層的クラスタリング  

    混合ガウスモデル（GMM)
        概要
            与えられたデータセットを、複数の正規分布の重ね合わせで表現する
            確率密度関数が得られる (確率分布として表現できる)
            サンプルごとに、各クラスターに所属する確率が得られる
            クラスター数を自動的に決められる
        利用方法
            クラスターの数を自動で決めたい
            データセットの確率密度が必要な時
        詳細
            クラスター数を振って、ベイズ情報量規準（BIC)の値が最小となるクラスタ数とする。

    その他
        AgglomerativeClustering
            凝集型クラスタリング 最も類似した２つのクラスタを併合していく。これを何らかの終了条件まで繰り返す。終了条件の連結度は、ward,average,complete。
        DBSCAN
            DBSCAN密度に基づくノイズあり空間クラスタリング
            param=min_sample, eps。あるデータポイントから距離eps以内にmin_sample以上のデータポイントがある場合。



# 参考
[データ解析に関するいろいろな手法・考え方・注意点のまとめ](https://datachemeng.com/summarydataanalysis/)  
