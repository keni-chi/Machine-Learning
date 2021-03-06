# classifier

アルゴリズム
    k-最近傍法
        小さいデータに関しては良いベースラインとなる。説明が容易。
    線形モデル
        LogisticRegression  Cを小さくなると係数を0に近づけることを重視。（正則化は強くなる。過剰適合を解消。）
        LinearSVM 同じくparam=C。他クラス分類の時は、2分類を組みわせる。
    ナイーブベイズクラス分類器
        GaussianNB
        BernoulliNB
        MultinomialNB
    決定木
    ランダムフォレスト
    勾配ブースティング
        GradientBoostingClassifier param=Learning_rate、大きくすると過剰適合側になる。param=n_estimators、大きくすると過剰適合側になる。尚、本では深さと学習率を変更している。
    サポートベクタマシン(SVMのSVC) ※回帰(SVMのSVR)もある。
        LinearSVM
        SVC param=C, gamma。gammaはガウシアンカーネルの幅を調整し、小さいと過剰適合を解消(RBFカーネル)。Cは線形モデルと同様の正則化パラメータであり、同様に小さいと過剰適合を解消。
    ニューラルネットワーク（ディープラーニング）

使い分け
    線形モデル
        最初に試してみるべきアルゴリズム。非常に大きいデータセットに適する。非常に高次元のデータに適する。
    ナイーブベイズモデル
        利点と欠点は線形モデルと共通する。長所は高速で理解しやすい。線形モデルですら時間がかかるデータへのベースラインモデルとして非常に有用。
        クラス分類にしか使えない。線形モデルよりもさらに高速。非常に大きいデータセット、高次元データに適する。線形モデルより精度が劣る事が多い。
    決定木
        長所は、「モデルが容易に可視化可能」「データのスケールに対して完全に不変（正規化、標準化不要）」決定木の問題点は、過剰適合しやすい。そのため、アンサンブルが用いられる。
        非常に高速。データのスケールを考慮する必要が無い。可視化が可能で説明しやすい。
    ランダムフォレスト
        勾配ブースティングとランダムフォレストでは、先にランダムフォレストを試した方がいいい。
        ランダムフォレストの場合、n_estimatorsは大きいほどよかったが、勾配ブースティングでは大きくすると過剰適合を招く。
        ほとんどの場合単一の決定木よりも高速で、頑健で、強力。データのスケールを考慮する必要が無い。高次元の疎なデータには適さない。
    勾配ブースティング
        多くの場合ランダムフォレストよりも少し精度が高い。ランダムフォレストよりも訓練に時間がかかるが、予測はこちらの方が早く、メモリ使用量も小さい。
        ランダムフォレストよりもパラーメータに敏感。
    SVM
        SVMでは特徴量の桁が違うと非常に大きな影響がある。そのため、前処理が重要。
        SVMは100,000サンプル以下くらいだとうまく機能する。サンプル少ない方が向いている。SVMは前処理とパラメータ調整が問題点。
        カーネル法を用いたSVMで重要なパラメータは、C、カーネルの選択、カーネル固有のパラメータである。RBFカーネルを使った場合、パラメータはgammaだけ。
        同じような意味を持つ特徴量からなる中規模なデータセットに対しては強力。データのスケールを調整する必要がある。パラメータに敏感。
    ニューラルネットワーク
        非常に複雑なモデルを構築できる。特に大きなデータセットに有効。データのスケールを調整する必要がある。
        パラメータに敏感。大きいモデルは訓練に時間がかかる。
