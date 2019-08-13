# etc

## 概要
覚書である。順次記載予定。  

### Jupyter Notebookでpip
!pip install xxx

### 形態素解析
janome

### Watson

#### Language Translator
curl -X POST -u "apikey:{apikey}" --header "Content-Type: application/json" --data "{\"text\": [\"Hello, world! \", \"How are you?\"], \"model_id\":\"en-es\"}" "{url}/v3/translate?version=2018-05-01"  

curl -X POST -u "apikey:{apikey}" --header "Content-Type: text/plain" --data "Language Translator translates text from one language to another" "{url}/v3/identify?version=2018-05-01"




## 参考

### ディープラーニング
[ディープラーニングこれだけは知っておきたい3つのこと](https://jp.mathworks.com/discovery/deep-learning.html)  
[パーセプトロンとは?](https://qiita.com/nishiy-k/items/1e795f92a99422d4ba7b)  

### 強化学習
[これから強化学習を勉強する人のための「強化学習アルゴリズム・マップ」と、実装例まとめ](https://qiita.com/sugulu/items/3c7d6cbe600d455e853b)  
[ゼロからDeepまで学ぶ強化学習](https://qiita.com/icoxfog417/items/242439ecd1a477ece312)  

### 自然言語処理
[AIが三国志を読んだら、孔明が知力100、関羽が武力99、を求められるのか？をガチで考える物語（自然言語処理編）](https://qiita.com/youwht/items/92056e63498c36de4e3b) 
[自然言語処理入門編！](https://qiita.com/cr-fun/items/cc82a85c572daac0b5c5)   
[自然言語処理入門 まとめ【Python + Janome + gensim】](https://qiita.com/kodera123/items/a5921cbcd18b9a309787)  

### 統計学
[統計WEB(統計学の時間)](https://bellcurve.jp/statistics/course/)  

### クラウド
[SoftLayer Bluemix Summit 2015: BluemixでWatsonをつかいたおせ！](https://www.slideshare.net/MikiYutani/softlayer-bluemix-summit-2015-bluemixwatson?qid=8fda4f26-b981-4268-8da5-192504fdc4a3&v=&b=&from_search=1)  
[【AI事始め】Watson APIをPythonで使ってみる（Language Translator）](https://qiita.com/kg1/items/88be91c5ecde8600220e)  
[watsonAPI LanguageTranslator で翻訳！！](https://qiita.com/van/items/8ab08bce0270baf377a2)  
