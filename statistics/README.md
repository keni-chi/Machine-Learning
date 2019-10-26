# statistics

## 概要
覚書である。順次記載予定。  

### pythonを用いた統計的仮説検定、信頼区間推定方法まとめ
- 3A. 分散分析(ANOVA)
- 母平均の信頼区間推定
- 母分散の信頼区間推定
- 4B. フリードマン検定(Friedman test)  
  対立仮説は「少なくとも１つの水準の母集団平均が他の水準の平均とは異なる」
- 3B. クラスカル・ウォリス検定(Kruskal-Wallis test)  
  対立仮説は「少なくとも１つの水準の母集団平均が他の水準の平均とは異なる」
- ルビーン検定(Levene's-test)  
  対立仮説は「少なくとも１つの水準の母集団分散が他の水準の母集団分散とは異なる」
- 1B. マン・ホイットニーのU検定(Mann-Whitney-U-test)  
  対立仮説は「2標本の間に差がある」
- 1A. 対応ありt検定(Paired-t-test)  
  対応するデータ間の差について「差の母平均は0である」という帰無仮説を検定する
- 2A. 対応なしt検定(Unpaired-t-test)  
  「2群の母集団の平均値(μ1,μ2)が等しい」という帰無仮説を検定
- 2B. ウィルコクソンの符号付き順位検定(Wilcoxon-Signed-rank-test)  
  対立仮説は「2標本の間に差がある」


## 参考
[統計WEB(統計学の時間)](https://bellcurve.jp/statistics/course/)  
[イカサマコインの例で最尤推定とベイズ推定の違いを理解してみる](https://qiita.com/MoriKen/items/09da26466c00500bcd68#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)  
[最尤推定量とは？初めての人にもわかる解説](https://to-kei.net/estimator/maximum-likelihood-estimation/)  
[5分でスッキリ理解するベイズ推定](https://qiita.com/HiromuMasuda0228/items/2dc62cf4f9dbdf373627)  
[統計初心者でも2分で雰囲気理解できるLME（線形混合）モデル](http://foslave.blogspot.com/2014/12/2lme.html)  
[Linear Mixed Model （以下、混合モデル）の短い解説](http://www.lowtem.hokudai.ac.jp/plantecol/akihiro/obenkyou/GLMMexample.pdf)  
[正規分布とは何なのか？その基本的な性質と理解するコツ](https://atarimae.biz/archives/9850)  

### パターン認識
[はじめてのパターン認識　目次](https://www.amazon.co.jp/dp/toc/4627849710/ref=dp_toc?_encoding=UTF8&n=489986)  
[はじめてのパターン認識　第１章](https://qiita.com/ssnnkkhh/items/34d024d56479d9c00f09)   
[はじめてのパターン認識　第2章](https://qiita.com/ssnnkkhh/items/a722b97ee9f9c061c4b7)
[はじめてのパターン認識　第3章 ベイズの識別規則 解説](https://qiita.com/icoxfog417/items/c3c8fed9902ad6200069)  
[はじめてのパターン認識 4章 確率モデルと識別関数（前半メモ）](https://qiita.com/golio/items/e0ab914701b9b006edda)  
[はじめてのパターン認識 第４章 確率モデルと識別関数　前半（観測データの線形変換）](https://qiita.com/sobeit@github/items/7234455c5ef04c8feb5b)  
[はじめてのパターン認識 第7章 パーセプトロン型学習規則](https://qiita.com/icoxfog417/items/e574a9d61f9f680d578b)  

### データ解析のための統計モデリング入門
[Pythonで実装しながら緑本を学ぶ (第2章 確率分布と統計モデルの最尤推定)](https://ohke.hateblo.jp/entry/2018/01/19/230000)  

### カーネル主成分分析
[カーネル主成分分析とは](https://qiita.com/NoriakiOshita/items/138c10eada03938fcd79)

### 統計学
[Pythonでt検定　2クラスの試験成績の比較](https://qiita.com/code0327/items/a96dd2fbd8a491d2eeaa)
[pythonを用いた統計的仮説検定、信頼区間推定方法まとめ](https://qiita.com/Wotipati/items/4f5e893fa39ad4cb9957)  
[パラメトリック検定とノンパラメトリック検定の違い](https://www.study-channel.com/2015/06/parametric-nonparametric-test.html)
[Pythonで母比率の95%信頼区間を区間推定し、妥当なサンプルサイズを決定する方法](https://tanuhack.com/estimate-pop-rate/)  
[Pythonでカイ二乗検定（適合度検定・独立性の検定）を行う方法 (Pythonによる統計学入門)](https://toukei.link/programmingandsoftware/statistics_by_python/chisqtest_by_python/)  

### ベイズ
[ベイズの定理とナイーブベイズ分類](https://hackmd.io/@fqZLfJuuS9O3vKeuZyZEfw/SkygLNZ-f?type=view)


### 相関係数
[【統計学】相関係数の検定（RとPython）](http://midsum-datasience.hatenablog.com/entry/2018/07/08/171113)  
[相関係数の検定(無相関検定)(notebookの一部)](http://lang.sist.chukyo-u.ac.jp/classes/PythonProbStat/Python-statistics4.html#RS04:correlationTest)