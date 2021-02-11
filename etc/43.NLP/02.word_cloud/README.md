# NLP

## 概要

### google colabでWordCloud

1. ライブラリをインストール
参考：ColaboratoryでMeCabを使えようにする　https://qiita.com/pytry3g/items/897ae738b8fbd3ae7893
※windowsではちょっと面倒そうだった。
!apt install aptitude
!aptitude install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file -y
!pip install mecab-python3==0.7

!pip install janome


2. MeCabの動作確認
参考：https://qiita.com/menon/items/f041b7c46543f38f78f7
import MeCab
m = MeCab.Tagger ("-Ochasen")
print(m.parse ("すもももももももものうち"))


3. フォントをダウンロード（窓の杜）
参考：https://forest.watch.impress.co.jp/library/software/ipafont/


4. フォントをアップロード
from google.colab import files
uploaded = files.upload()
上記を実行し、ttcファイルを選択。


5. ソースコード
参考：https://qiita.com/yuuuusuke1997/items/122ca7597c909e73aad5


6. ソースコードを修正
テキスト取得のfor文は時間短縮のため、breakを入れる。
WordCloud()内の、font_pathの引数は、'ipag.ttc'等とする。




