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



## 参考
[【秒速で無料GPUを使う】深層学習実践Tips on Colaboratory](https://qiita.com/tomo_makes/items/b3c60b10f7b25a0a5935)
[環境構築不要でPython入門！Google Colaboratoryの使い方を分かりやすく説明](https://cpp-learning.com/python_colaboratory/)  
[【秒速で無料GPUを使う】TensorFow(Keras)/PyTorch/Chainer環境構築 on Colaboratory](https://qiita.com/tomo_makes/items/f70fe48c428d3a61e131)
