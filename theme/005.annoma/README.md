# annomaly

外れ値検出
    ３σ法
        データが正規分布を仮定している
        問題として、外れ値を含んで平均や標準偏差が計算される
    Hampel Identifier
        データが正規分布を仮定している
        外れ値にロバストな統計量を使用。
        中央値、中央絶対偏差の1.4826倍
    平滑化(スムージング)による外れ値検出
        時系列データの外れ値検出で有効な方法
    データ密度による外れ値(外れサンプル)検出
        複数の変数を利用できる
            SVM
                データ分布に違いがあると対応が難しい
                次元の呪いの影響を受けにくい
            K近傍
                データ分布に違いがあると対応が難しい
                次元の呪いの影響を受ける
            Local Outlier Factor (LOF) 
                データ分布に違いがあってもOK
                次元の呪いの影響を受ける
        多変量プロセス管理
            主成分分析
            独立分析分析
            T2統計量・・・主要な主成分のみを分散１に規格化して、T2統計量を監視指標の１つとして用いる。
            Q統計量・・・T2統計量で監視されない、主要でない主成分については、Q統計量を用いる。二乗予測誤差（Squared Prediction Error: SPE）。


# 参考
[データ解析に関するいろいろな手法・考え方・注意点のまとめ](https://datachemeng.com/summarydataanalysis/)  
[時系列データの外れ値検出](https://qiita.com/hoto17296/items/d337fe0215907432d754)  
[【データ分析入門】機械学習未使用！Pythonでゼロから始める振動解析](https://cpp-learning.com/vibration-analysis/)  
[【信号処理入門】機械学習未使用！Hampelフィルタで外れ値検出（異常検知） -Python-](https://cpp-learning.com/hampel-filter/)  
[Pythonで高速フーリエ変換（FFT）の練習-1 簡単な信号でFFTを体験してみよう](https://momonoki2017.blogspot.com/2018/03/pythonfft-1-fft.html)  
[【python】sklearnのOneClassSVMを使って外れ値検知してみる](https://www.haya-programming.com/entry/2018/12/14/111126)  

