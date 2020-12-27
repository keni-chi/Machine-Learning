# Feature engineering


カテゴリー:
    目的変数
        X-means: 新しいクラスタを作り分類に落とす
        target encoding:　
            ある特徴量の目的変数の相対頻度 (割合) を計算。
            一般的に説明変数に含まれるカテゴリ変数ごとの、目的変数の平均値を特徴量として用いる
        ラベルエンジニアリング:
            2値変数を回帰問題にするためにスコアリングする
    説明変数単体
        演算
            count encoding: 各ラベルを、訓練データ内でのそのラベルの発生頻度に置き換える
            label-count encoding: count encoding をさらに、頻度の大きさの順位に変換する
            NaN encoding: NaNという一つのbooleanの特徴量として扱う
            expansion encoding:　「ユーザーは最新のバージョンを使っているか？」→1(使用している) 0(使用していない)
    説明変数複数
        Polynominal encoding: カテゴリ変数同士の関係を元に作る。XOR。
    その他
        Label encoding: 全てのカテゴリに数値によるIDを割り当てる
        One-hot encoding:　カテゴリごとにBooleanで表現
        hash encoding: 
        データクリーニング
            展開変換 expansion endoding
            連結変換 consolidation encoding

数値:
    目的変数
        ラベルエンジニアリング:
            対数/指数変換
            2乗変換
            Box-Cox transformation:　　ロングテイルなデータを持っている場合はログ変換
    説明変数単体
        演算
            Rounding:　連続値の場合は、ある程度のところで四捨五入する
            scaling:　Standard(Z) Scaling, MinMax Scaling, Root Scaling, Log scaling
            sigmoid / tanh / log transformations: 
        その他
            binning:　連続値の場合に、ある特定のレンジを決めて、レンジごとにカテゴリを分ける手法
            Trendlines:　「売上総額」を特徴量にするのではなくて「先週の売上」「先月の売上」「過去10年の売上」など「傾向」をモデルに与える
    説明変数複数
        Interaction:　四則演算
        非線形変換することで線形モデルへの当てはまりを良くする方法:
            多項式カーネル
            leafcoding
            遺伝的アルゴリズム
            局所線形埋め込み, スペクトル埋め込み, t-SNE
        行ごとの統計量を特徴量:
            欠損値の数
            ゼロの数
            負値の数
            平均最大最小歪度その他
    その他
        imputation:　欠損値補完（平均など）

時間変数:
    循環的な変換: 週、月の日付のように循環する数値を, 円の座標のように循環する2つの変数に置き換える
    トレンドを取り出す: 例えば購入額の総計を, 週末の値, 月末の値などにすると, 総額が同じでも購入額が増えていく顧客と減っていく顧客を区別できる
    大きなイベントからの距離:    祝日の何日前/後かを表す特徴量を作る
    過去データ:

空間変数:
    GPS座標、都市、国や地域、住所など

その他:
    Consolidation encoding:　名寄せ
    model stacking: 複数の予測モデルのアンサンブル
    Random Feature Elimination:
    Downsampling/ Upsampling:


# 参考
[特徴量エンジニアリング備忘録](https://qiita.com/risako_/items/91ea7f34433bfa2ea40c)  
[Target Encoding のやり方について](https://blog.amedama.jp/entry/target-mean-encoding-types)  
[HJvanVeenの『特徴量エンジニアリング』註解](https://qiita.com/s_katagiri/items/492f86529f3c02905e76)

