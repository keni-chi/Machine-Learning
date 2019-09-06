# cloud

## 概要
覚書である。順次記載予定。  

### Watson

#### Language Translator
curl -X POST -u "apikey:{apikey}" --header "Content-Type: application/json" --data "{\"text\": [\"Hello, world! \", \"How are you?\"], \"model_id\":\"en-es\"}" "{url}/v3/translate?version=2018-05-01"  

curl -X POST -u "apikey:{apikey}" --header "Content-Type: text/plain" --data "Language Translator translates text from one language to another" "{url}/v3/identify?version=2018-05-01"

## 参考
[SoftLayer Bluemix Summit 2015: BluemixでWatsonをつかいたおせ！](https://www.slideshare.net/MikiYutani/softlayer-bluemix-summit-2015-bluemixwatson?qid=8fda4f26-b981-4268-8da5-192504fdc4a3&v=&b=&from_search=1)  
[【AI事始め】Watson APIをPythonで使ってみる（Language Translator）](https://qiita.com/kg1/items/88be91c5ecde8600220e)  
[watsonAPI LanguageTranslator で翻訳！！](https://qiita.com/van/items/8ab08bce0270baf377a2)  
[Watson API 目次](https://www.ibm.com/blogs/solutions/jp-ja/watson-api-matome/#section1)  
