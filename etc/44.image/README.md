
## 姿勢推定

トラッキング
    概要
        動画の元とな１コマ（１フレーム）の画像中に，ある特定の人物や車といったオブジェクトを見つけることができた時，次のフレームでも，その次のフレームでも，一度見つけたオブジェクトを追い続けるというタスク
    難しいポイント
        例えば数秒単位だと被写体が時間の間に移動する距離が大きくなり追いかけるのが大変
        時間をまたいで同じ人を追跡し続けるための表現を何かしら得ること


DeepCut
    肘や膝といった人体を構成する部分をキーポイントとして最初に抽出し，抽出したキーポイント同士をうまくつなげるというボトムアップ型のアプローチ

DeeperCut
    ステージという単位を用いて，１ステージ目で上半身，２ステージ目で下半身といった段階に分けた抽出を行う工夫を取り入れ 

ArtTrack
    姿勢推定問題とトラッキング問題を同時に解く
    空間的なマッチングに加えて時間的なマッチングも行うという問題設定が追加されている
    高速処理の工夫
        まず人物の頭部を検出し，その後頭部に応じて，他のキーポイントを抽出し，Non Maximum Supression(NMS)を使って部分抽出を行う
            DeeperCutまでのキーポイント抽出機では，まずキーポイントの候補点をひたすらに出力するような仕組みで動いていました．そうすると，キーポイントが出た後に，マッチング問題を考える上で，組み合わせ数が膨大になってしまう問題が発生していました．
            ArtTrackでは，先に人物の頭部のみを検出し，その周辺のキーポイントを抽出することで，キーポイントの抽出と人物の特定を別々に行なっていたボトムアップ型のアプローチと異なり，マッチングの際の計算コストを減らすことが可能となります．さらに，DeeperCutでも使用した，階層的なキーポイントの抽出構造を以下の画像のように使用することで，より精度の高いキーポイント抽出が可能となっています．

マッチングの工程
    この部分に処理時間がかかってしまうということがArtTrackやOpenPoseが出る前までの問題
    Temporal edge・・・時間的なつながり。時刻tの時の頭部と，時刻t+1の時の頭部をつなげる。
    Spatial edge・・・同じフレーム内でのつながり







## 参考
[【MNIST】データ拡張で汎化性能UPっぷ！](https://qiita.com/PoodleMaster/items/54c184d9f2f70cc011d0)  
[pythonで __new__() を使いdictから特定のクラスのインスタンスを作成する方法](https://qiita.com/podhmo/items/5183ac68fee353192ca5)  
[インスタンス変数を辞書型で出力 + JSON形式で文字列にする](https://kuzunoha-ne.hateblo.jp/entry/2019/01/25/213300)  
[python - RGB画像(3チャネル)をグレースケール(1チャネル)に変換して保存する方法は？](https://cloud6.net/so/python/3052021)   
[Keras - Keras の ImageDataGenerator を使って学習画像を増やす](https://pynote.hatenablog.com/entry/keras-image-data-generator)  
[【ミニバッチ学習と学習率】低バッチサイズから始めよ](https://dajiro.com/entry/2020/04/15/221414)  
[Kaggle Digit Recognizer にCNNで挑戦、公開Kernelの中で最高精度を目指す](https://qiita.com/corochann/items/e83029d1ad94d908e220)    

## 姿勢推定
[ArtTrack_github](https://github.com/eldar/pose-tensorflow)  
[ArtTrack論文紹介](https://www.glia-computing.com/blog/arttrack-articulated-multi-person-tracking-in-the-wild/)  
[論文まとめ：PoseTrack: Joint Multi-Person Pose Estimation and Tracking](https://qiita.com/masataka46/items/bcbd68441b7800596835)  

## tf-pose-estimation
[Windowsで姿勢推定(tf pose estimation)](https://qiita.com/kayu0516/items/754c6719fb55d2a6d563)  

# openpose
[openpose_github](https://github.com/CMU-Perceptual-Computing-Lab/openpose)  
