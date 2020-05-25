# keras

Keras
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



[SequentialモデルでKerasを始めてみよう](https://keras.io/ja/getting-started/sequential-model-guide/)


