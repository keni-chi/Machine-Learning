# DL

4.ニューラルネットワークの学習
    4.2.損失関数
        4.2.1. 2乗和誤差
        4.2.2. 交差エントロピー誤差
        4.2.3. ミニバッチ学習
            交差エントロピー誤差の場合、4.3式のように書ける。
        4.2.5. なぜ損失関数を設定するのか？
            「認識精度」を指標にすべきではないか、という疑問について。
                ・学習時に最適なパラメータを探索する際、損失関数が小さくなるようなパラメータ値を探す。
                そのため、パラメータの微分（正確には勾配）を計算し、その微分値を手掛かりにパラメータ値を徐々に更新していく。
                ・認識精度を指標にしてはいけない理由は、微分がほとんどの場所で０になってしまい、パラメータの更新ができなくなってしまうから。
                なぜ０になってしまうかというと、パラメータを少し変えても精度は32%のままになってしまう。また、33,34のように不連続な値となってしまう。
                即ち、ステップ関数のように微分が０となってしまうことが多くなる。シグモイド関数だと、どこでも微分が０とならず、正しい学習が行えるようになる。
    4.4.勾配
        4.4.1.勾配法
    4.5.学習アルゴリズムの実装
        確率的勾配降下法（SGD)
            ミニバッチとして無作為に選ばれたデータを使用している。
5.誤差逆伝播法
    5.3.逆伝播
        5.3.1.加算ノードの逆伝播
            そのまま流す
        5.3.2.乗算ノードの逆伝播
            入力信号をひっくり返した値を乗算する。そのため、順伝播の入力信号を保持する。
    5.5.活性化関数レイヤの実装
        5.5.1 ReLUレイヤ
        5.5.2 Sigmoidレイヤ
    5.6 Affine/Softmaxレイヤの実装
        5.6.1 Affineレイヤ
            アフィン変換は、行列の積のこと。
            逆伝播は5.13式。導出は略。
        5.6.2 バッチ版Affineレイヤ
        5.6.3 Softmax-with-Lossレイヤ
    5.7 誤差逆伝播法の実装
        5.7.1 ニューラルネットワークの学習の全体図
            ステップ１（ミニバッチ）
            ステップ２（勾配の算出）・・・各重みパラメータに関する損失関数を求める
            ステップ３（パラメータの更新）・・・重みパラメータを勾配方向に微少量だけ更新する
            ステップ４（繰り返す）・・・１～３の繰り返し
6.学習に関するテクニック
    6.1 パラメータの更新
        6.1.2 SGD
        6.1.4 Momentum
        6.1.5 AdaGrad
        6.1.6 Adam
    6.2 重みの初期値
    6.3 Batch Normalization
    6.4 正則化
        6.4.2 Weight decay
            大きな重みを持つことに対してペナルティを課す
7.畳み込みニューラルネットワーク
    7.7 代表的なCNN
        7.7.1 LeNet
        7.7.2 Alexnet
            LeNetとの違いは以下。
                活性化関数にReLU
                LRNという局所的正規化を行う層を用いる
                Dropoutを使用
8.ディープラーニング
    
