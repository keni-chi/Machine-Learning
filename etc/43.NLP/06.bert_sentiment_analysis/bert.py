# Python 3.9.7

from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer

# パイプラインの準備
model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment') 
tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
nlp = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)

# 感情分析の実行
print(nlp("私はとっても幸せ"))
print(nlp("私はとっても不幸"))
