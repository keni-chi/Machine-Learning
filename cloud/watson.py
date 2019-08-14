#  -*- coding: utf-8 -*-
import json
from watson_developer_cloud import LanguageTranslatorV3 as LanguageTranslator

language_translator = LanguageTranslator(
  version='2018-12-03',
  iam_apikey='{key}',
  url='{url}'
)

num = 0
while (num < 1):
    text = input('和英翻訳するよ。日本語か英語を入力してね。\n')
    # 言語識別
    language = language_translator.identify(text).get_result()
    source = language['languages'][0]['language']
    if source == 'en':
        target = 'ja'
    elif source == 'ja':
        target = 'en'
    else :
        source = 'ja'
        target = 'en'
    # 翻訳
    translation = language_translator.translate(
        text=text,
        source=source,
        target=target)
    print(translation.result['translations'][0]['translation'])
    print()
    num += 1
