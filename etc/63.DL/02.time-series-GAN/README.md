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