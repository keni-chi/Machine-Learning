# pytorch

## 概要
pip install torch===1.6.0 torchvision===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html

特徴
    Tensorflow、Kerasは静的フレームワークだが、pytorchは動的フレームワーク。
動的フレームワーク長所
    直感的に書くことができる
    デバッグがしやすい
    サンプル毎に構造が変化するような複雑なネットワーク の実装が簡単にできる（TreeRNNs等）
動的フレームワーク短所
    サンプル毎に毎回計算グラフを構築するため、学習速度が少し遅くなる


## 参考
[PyTorchでシンプルな多層ニューラルネットワークを作ろう](https://qiita.com/sudamasahiko/items/b54fed1ffe8bb6d48818)  
[ディープラーニング初心者がPyTorchを選んだ3つの理由](https://watlab-blog.com/2020/01/26/pytorch/)  
