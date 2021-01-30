# sampling

SMOTENC
    特徴量に、連続値と離散値(カテゴリ値)が混在するデータセットを扱うときに使用
    Synthetic Minority Over-sampling Technique for Nominal and Continuousの略
BorderlineSMOTE
	少数派サンプル群と非少数派サンプル群との境界を利用し、最近傍法でサンプルを生成(SMOTEアルゴリズムに類似)
SVMSMOTE
	SVM分類器を使用してサポートベクトルを見つけ、それらを考慮したサンプルを生成
KMeansSMOTE
    SMOTEを適用する前にKMeansクラスタリング手法を使用する


# 参考
[【前処理の学習-36】データを学ぶ ～生成～④](https://pimientito-handson-ml.hatenablog.com/)  

