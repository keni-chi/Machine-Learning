## 実装メモ

### マウントしてドライブから読み込み
from google.colab import drive  
drive.mount('/content/drive')  
df = pd.read_csv('drive/My Drive/Colab Notebooks/data.csv')  

### 3次元を2次元に変換してdriveに保存
newarr = synth_data.reshape(3661*24, 6)  
df_out = pd.DataFrame(newarr)  
df_out.to_csv('drive/My Drive/Colab Notebooks/df_out.csv')  
df_out.head()  



## 参考
[TimeGAN colab](https://colab.research.google.com/github/ydataai/ydata-synthetic/blob/master/examples/timeseries/TimeGAN_Synthetic_stock_data.ipynb)  
[TimeGAN github](https://github.com/ydataai/ydata-synthetic)   
[時系列データ生成RTSGANの実装方法](http://blog.livedoor.jp/tak_tak0/archives/52439130.html)  
[時系列にもGAN](https://ai-scholar.tech/articles/time-series/GAN_for_time-series)  
[tadgan異常検知](https://github.com/arunppsg/TadGAN)  
[PyTorchによるTadGAN（時系列異常検知）](https://zenn.dev/yonda/articles/681f32264341cf)  
[tadgan arxiv](https://arxiv.org/pdf/2009.07769.pdf)  
[tadgan 記事](https://engineer.fabcross.jp/archeive/210122_hidden-warning-signals.html)  


## 補完
[深層学習を用いた時系列補間技術の非画像データへの適用性評価](https://www.mss.co.jp/technology/report/pdf/29_01.pdf)
