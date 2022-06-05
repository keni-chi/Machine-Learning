# keras

### Keras
    活活性化関数
        あるニューロンが複数の(各ニューロンごとに重みがついた)ニューロンからの入力を受け取り、受け取った値を合計した後 そのニューロン自身を0～1の間の値に落とし込むための関数。
    コンパイル
        モデルの学習を始める前に，compileメソッドを用いどのような学習処理を行なうかを設定
            最適化アルゴリズム
            損失関数: モデルが最小化しようとする目的関数
            評価関数のリスト
        実装例
            # マルチクラス分類問題の場合
            model.compile(optimizer='rmsprop',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
            # 2値分類問題の場合
            model.compile(optimizer='rmsprop',
                        loss='binary_crossentropy',
                        metrics=['accuracy'])
            # 平均二乗誤差を最小化する回帰問題の場合
            model.compile(optimizer='rmsprop',
                        loss='mse')

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
Knowledge Distillation
    知識蒸留は、モデル圧縮の手順。
    学生モデルと教師モデルを構築。
Metric learning for image similarity search
    画像類似検索のためのメトリック学習
    データ間の関係性を考慮した特徴量空間を学習する手法
Point cloud classification with PointNet
    PointNetは点群処理モデル。
    クラス分類、セグメンテーション、検出など応用範囲が広く、与えられた点群全体に対してクラス分類を行うこともできるし、点群をセグメントに分割し、それぞれのセグメントに対してラベル付けすることもできる。
    上段でクラス分類を行い、下段ではsemantic segmentationやpart segmentationを行う。
Few-Shot learning with Reptile
    少ないデータでの学習
Object Detection with RetinaNet
    RetinaNetによるオブジェクト検出
    物体検出モデルは、「単一ステージ」と「2ステージ」の検出器に大きく分類される
    正確で高速に実行される人気のある1ステージ検出器


## 参考
[SequentialモデルでKerasを始めてみよう](https://keras.io/ja/getting-started/sequential-model-guide/)
[Keras チュートリアル](https://qiita.com/sasayabaku/items/64a01363bcd5c44feb0b)  
[脳死で覚えるkeras入門](https://qiita.com/wataoka/items/5c6766d3e1c674d61425)
[kears_Code examples_(公式)](https://keras.io/examples/)  
[【Python】KerasでVGG16を使って画像認識をしてみよう！](https://www.y-shinno.com/keras-vgg16/)  

# fine tuning
[kerasのfashion_mnistで転移学習](https://snova301.hatenablog.com/entry/2019/05/26/203003)  
[KerasでVGG16のファインチューニングを試してみる](https://qiita.com/ps010/items/dee9413d3de28de7d2f9)  
[【MNIST】ImangeNetのモデルを利用してFineTuningやってみた【効率的な高精度モデルの構築】](https://qiita.com/PoodleMaster/items/a98344e22327130791d8)  
