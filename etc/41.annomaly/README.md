# annomaly

外れ値検出手法
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
                データ分布に違いがあってもOK(K近傍と比較してデータ分布における局所密度の違いを考慮できる)
                次元の呪いの影響を受ける
        多変量プロセス管理
            主成分分析、独立分析分析で外れデータ点を見つける。以下統計量を用いるこもできる。
                T2統計量・・・主要な主成分のみを分散１に規格化して、T2統計量を監視指標の１つとして用いる。
                Q統計量・・・T2統計量で監視されない、主要でない主成分については、Q統計量を用いる。二乗予測誤差（Squared Prediction Error: SPE）。


# 参考
[データ解析に関するいろいろな手法・考え方・注意点のまとめ](https://datachemeng.com/summarydataanalysis/)  
[時系列データの外れ値検出](https://qiita.com/hoto17296/items/d337fe0215907432d754)  
[【データ分析入門】機械学習未使用！Pythonでゼロから始める振動解析](https://cpp-learning.com/vibration-analysis/)  
[【信号処理入門】機械学習未使用！Hampelフィルタで外れ値検出（異常検知） -Python-](https://cpp-learning.com/hampel-filter/)  
[Pythonで高速フーリエ変換（FFT）の練習-1 簡単な信号でFFTを体験してみよう](https://momonoki2017.blogspot.com/2018/03/pythonfft-1-fft.html)  
[【python】sklearnのOneClassSVMを使って外れ値検知してみる](https://www.haya-programming.com/entry/2018/12/14/111126)  
[異常検知入門と手法まとめ](https://qiita.com/toucan/items/c3343de3cfa236df3bda#probability-approach)  
[時系列異常検知SOTAサーベイ](https://ai-scholar.tech/articles/survey/ad_survey)  
[異常検知入門2　外れ値検出](https://qiita.com/ngayope330/items/fc941b8d49b90319748e#1%E3%82%AF%E3%83%A9%E3%82%B9svm%E3%81%A8%E3%81%AF)  
[【具体例あり】機械学習を用いた異常検知の手法と学習モデルを解説！](https://www.tryeting.jp/column/1405/#i-3)  

### 密度比
[異常検知と変化検知のまとめ　数式なし](https://qiita.com/GushiSnow/items/f032806cfa8cec046318)  
[密度比推定による変化検知](https://qiita.com/ground0state/items/0814497e190a6f666144)  

### ホテリングのT2
[最も簡単な異常検知の手法-ホテリングのT2 理論](https://masamunetogetoge.com/hotelling-t2)  
[T二乗法](http://harmonizedai.com/article/t%E4%BA%8C%E4%B9%97%E6%B3%95/)  
[Pythonでお手軽・異常検知 [ホテリング理論編]](https://qiita.com/Zepprix/items/f6a5de2e3f6689bd2c1f)  


### scipy.statsのintervalとppf 
[scipy.statsのメソッドまとめ](https://ai-soldier.work/scipy-stats-method/#toc_id_3_2)  
[intervalが正しそう](https://www.kabuku.co.jp/developers/anomaly-detect)  


### VAE
[VAEの異常検知の精度向上を考える](https://qiita.com/maharuda/items/9e9ef8ab021a2cb18573)  

### 異常検知・変化点検知
[統計的異常検知/変化検知の基本をまとめる](https://www.procrasist.com/entry/21-anomaly-detection)  
