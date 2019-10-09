# etc

## 概要
覚書である。順次記載予定。  


## 参考

### トピック別

### 前処理
[最低限知っておくべきデータの前処理](https://qiita.com/kazukiii/items/2600987798c62dd29dfc)  
[機械学習における欠損値補完について考える](https://rmizutaa.hatenablog.com/entry/2019/06/30/212103)  


#### アンサンブル学習
[XGBoostの主な特徴と理論の概要](https://qiita.com/yh0sh/items/1df89b12a8dcd15bd5aa)  
[LightGBM ハンズオン - もう一つのGradient Boostingライブラリ](https://qiita.com/TomokIshii/items/3729c1b9c658cc48b5cb)  

#### ディープラーニング
[ディープラーニングこれだけは知っておきたい3つのこと](https://jp.mathworks.com/discovery/deep-learning.html)  
[パーセプトロンとは?](https://qiita.com/nishiy-k/items/1e795f92a99422d4ba7b)  
[PyTorchとは？概要と導入方法をチェックしよう！](https://www.sejuku.net/blog/64175)  

#### 強化学習
[これから強化学習を勉強する人のための「強化学習アルゴリズム・マップ」と、実装例まとめ](https://qiita.com/sugulu/items/3c7d6cbe600d455e853b)  
[ゼロからDeepまで学ぶ強化学習](https://qiita.com/icoxfog417/items/242439ecd1a477ece312)  
[CartPoleでQ学習（Q-learning）を実装・解説【Phythonで強化学習：第1回】](http://neuro-educator.com/rl1/)  

#### 自然言語処理
[形態素解析のライブラリ「Mecab」と「Janome」を使ってみよう](https://ushinji.hatenablog.com/entry/2017/11/23/161031)  
[自然言語処理における前処理の種類とその威力](https://qiita.com/Hironsan/items/2466fe0f344115aff177)  
[AIが三国志を読んだら、孔明が知力100、関羽が武力99、を求められるのか？をガチで考える物語（自然言語処理編）](https://qiita.com/youwht/items/92056e63498c36de4e3b) 
[自然言語処理入門編！](https://qiita.com/cr-fun/items/cc82a85c572daac0b5c5)   
[自然言語処理入門 まとめ【Python + Janome + gensim】](https://qiita.com/kodera123/items/a5921cbcd18b9a309787)  
[データ解析: LDAの実装(gensim)](https://openbook4.me/projects/193/sections/1154)  
[「言語処理のための機械学習入門」"超"まとめ](https://qiita.com/yuyasat/items/66d057b1b91722c85aa3)  
[自然言語（日本語）処理](http://www.sist.ac.jp/~kanakubo/research/natural_language_processing.html)  
[自然言語処理（NLP）ってなんだろう？](https://qiita.com/MahoTakara/items/b3d719ed1a3665730826)  
[AIはハチ=米津玄師を見破れるか ? -J-popアーティストの歌詞を分析してみた-](https://qiita.com/kazuya-n/items/0a2fe586716c925055d1)  
[Word2Vecを用いた類義語の抽出が上手く行ったので、分析をまとめてみた](https://qiita.com/To_Murakami/items/cc225e7c9cd9c0ab641e)  
[日本語WordNetを使って、類義語を検索できるツールをpythonで作ってみた](https://qiita.com/pocket_kyoto/items/1e5d464b693a8b44eda5)  
[自然言語 Wordnet × Pythonで類義語を抽出する](https://www.yoheim.net/blog.php?q=20160201)  


### ライブラリ別

#### 概要
[Dockerを使って機械学習実行環境（勾配ブースティング、ニューラルネット含む）を30分で構築する - python, Mecab, LightGBM, xgboost, TensorFlow, keras, Pytorch, etc](https://www.takapy.work/entry/2019/04/07/134433)  

#### LightGBM
[Light GBMを使うとOMPエラーでカーネルが死ぬ](https://haltaro.github.io/2018/06/22/dead-kernel-lgbm)  
[【Mac】gccのバージョン確認、新しいバージョン（8.2.0）をインストール](https://qiita.com/aki-takano/items/0152a3ab4a615cfef9bc)  
[MacbookにLightGBMをインストールする](https://ymegane88.hatenablog.com/entry/2018/12/13/005342)  

#### genism
- トピックモデリング用ライブラリ
- 単語の並びなどを忘れて、単純に文書内にそれぞれの単語が何回出現したかという出現回数の情報だけを保持する  

#### Mecab and Janome
- 形態素解析のライブラリ
- Janomeはpipコマンドで簡単に導入できる点がメリット。実行速度は劣る。

#### hdf5
- NumPy から扱えるデータをファイルに保存するためのフォーマット<br><br>
[h5py の簡単な使い方](https://www.qoosky.io/techs/861b4ae419)  

#### Pillow
[Pythonの画像処理ライブラリPillow(PIL)の使い方](https://note.nkmk.me/python-pillow-basic/)

#### Sympy
- Sympy...代数計算ライブラリ  
[Sympy+Jupyterで最強の電卓環境を作る](https://qiita.com/pashango2/items/500d23c8f43784b54315)  
