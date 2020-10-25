# NLP

## 概要

Transformer
    2017年の6月、 Attention Is All You Need という強いタイトルの論文が Google から発表
        (Attention は従来の RNN のモデル Seq2Seq などでも使われていました)
        Transformer は文章などのシーケンスから別の文章などのシーケンスを予測するモデルとして発表されました
    単語の位置をベクトルとして表現し入力単語に足すことで位置情報を付与(LSTMは直近だけ)

BERT
    概要
        学習に残す単語は何がよいか、BERTは全体で予測用をランダム15%で検証。全体の行列計算。
        複数のタスクで人間を上回る性能を記録
            Transformerを複数結合させ、双方向で言語モデルを学習
        現在の自然言語処理では単語や文を意味を考慮した数値に変換させることが重要です。BERTはここで活躍。
    仕組み
        簡単な処理を追加
            ２つの文が連続するかどうか
                2つの文を結合させて入力し、出力される文のベクトルを使って連続かどうかのラベルを予測
            文の分類
                文を入力し、文ベクトルを使ってクラスラベルを予測
            質問応答
                質問文と知識結合させて入力し、知識のどこからどこまでが解答に当たるかを予測（解答の開始と終わりのクラスを予測）
            固有表現識別（人物、組織、場所など）
                各単語にその固有表現のクラスを予測する
    学習
        マスク単語予測
            文中のランダムで選ばれた15％の単語をマスクして、それを予測します
            これにより単語の意味や単語同士の関係性を学習できると期待されます
        連続文予測
            2つの文が連続しているかどうかを予測
            これにより文の構造を学習できることが期待されます
    以降
        そもそもマスクする単語はランダムでよいのか
        連続文の解釈は範囲が広すぎるため工夫できないか
        、など様々な工夫がされています



# 参考
[作って理解する Transformer / Attention](https://qiita.com/halhorn/items/c91497522be27bde17ce)  
[今更ながらchainerでSeq2Seq（2）〜Attention Model編〜](https://qiita.com/kenchin110100/items/eb70d69d1d65fb451b67)  
[2019年はBERTとTransformerの年だった](https://ainow.ai/2020/02/25/183082/)  
[Longformer: The Long-Document Transformer](https://github.com/reo11/papers100knock/issues/35)  
[最近のDeep Learning (NLP) 界隈におけるAttention事情](https://www.slideshare.net/yutakikuchi927/deep-learning-nlp-attention)  
[自然言語処理でBERTまでの流れを簡単に紹介](https://nmoriyama.hatenablog.com/entry/2020/01/24/160351)  
[自然言語処理の王様「BERT」の論文を徹底解説](https://qiita.com/omiita/items/72998858efc19a368e50)
