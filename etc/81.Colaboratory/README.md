# Colaboratory

## 概要
覚書である。順次記載予定。  

### Colaboratory
GPUの使い方
編集→ノートブックの設定

経過時間の確認
!cat /proc/uptime | awk '{print $1 /60 /60 /24 "days (" $1 / 60 / 60 "h)"}'

ディスク空き容量
!df -h

メインメモリ
!free -h

GPUメモリの利用状況
!nvidia-smi

!apt-get install sysstat #sarの準備
!free -tm #メモリ空き
!ps aux #プロセス実行状況
!top # 各プロセスのリソース使用状況
!sar -u -r 1 5 #メモリ、CPU利用率の履歴

### Kerasチュートリアル
犬猫の画像の分類
CNNでMNIST
U-NetでSemantic Segmentation（画像を画素レベルで把握。画像内の各画素をオブジェクトクラスに割り当てようとすること。）
OCR(画像データから文字を認識して、機械が読み取れる形に変換する技術）のモデル・・・CNNとRNNを組み合わせたモデル
Conv-LSTM
Grad-CAMで、象の画像について視覚化（モデルの解釈）。
    画像分類モデルのクラスアクティベーションヒートマップを取得する（CNNが分類のために注視している範囲をカラーマップで表示）。
    予測クラスのoutput値に寄与の大きいところ(勾配の大きいところ)が分類予測を行う上で、重要な箇所という考え。
EfficientNetを使用したfine-tuningによる画像分類
Integrated Gradientsで、象の画像について視覚化（モデルの解釈）。
    ニューラルネットワークがどのように画像内の物体を捉えているのかを理解するのはほぼ不可能ですが、ブラックボックスの挙動を理解しようとする試みは日々続けられています。
    画像を入力とするニューラルネットワークでは、ネットワークがどのように画像内の物体を捉えているのかを可視化することによって、どのような特徴を捉えているのかを理解したり、ネットワークの性能改善の指針として役立てられています。
    ネットワークがどのように画像内の物体を捉えているのかを画像化したものは顕著性マップと呼ばれたりします。


## 参考
[【秒速で無料GPUを使う】深層学習実践Tips on Colaboratory](https://qiita.com/tomo_makes/items/b3c60b10f7b25a0a5935)
[環境構築不要でPython入門！Google Colaboratoryの使い方を分かりやすく説明](https://cpp-learning.com/python_colaboratory/)  
[【秒速で無料GPUを使う】TensorFow(Keras)/PyTorch/Chainer環境構築 on Colaboratory](https://qiita.com/tomo_makes/items/f70fe48c428d3a61e131)

[Keras チュートリアル](https://qiita.com/sasayabaku/items/64a01363bcd5c44feb0b)  
[脳死で覚えるkeras入門](https://qiita.com/wataoka/items/5c6766d3e1c674d61425)
[kears_Code examples_(公式)](https://keras.io/examples/)  

[【PyTorch】チュートリアル(日本語版 )① 〜テンソル〜](https://qiita.com/Hexans/items/bb0f95c0c180f696a598)  
[【PyTorchチュートリアル①】What is PyTorch?](https://qiita.com/sudominoru/items/544aec4dc867187a93fa)  
