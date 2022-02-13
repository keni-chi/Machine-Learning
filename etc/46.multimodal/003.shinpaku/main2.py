import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import seaborn as sns
import os
import shutil
from scipy import signal
import glob
from scipy import fftpack

p1_list = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', '1100', '1200', '1300', '1400', '1500']
save_list = []

for param1 in p1_list:

    #画像ファイルを格納，時系列にソート
    files = glob.glob("IMG_5666_myaku_midori_" + param1  + "/*.png")
    files.sort()

    #画像を読み込み，green成分を抽出
    images = [cv2.imread(files[i]) for i in range(len(files))]
    images_green = [pd.DataFrame(images[j][:,:,1]) for j in range(len(images))]
    print(images_green[0])

    # 1920*1080
    #parameter
    in1 = 1000
    in2 = 1400
    co1 = 300
    co2 = 500

    #メディアンフィルタによる平滑化
    images_green_median = [cv2.medianBlur(images_green[i].iloc[ in1 : in2 , co1 :co2 ].values,ksize=5)  for i in range(len(images_green))]

    #平均値を算出
    img_mean = [images_green_median[i].mean()  for i in range(len(images_green_median))]
    print(img_mean)
    # s = pd.Series(img_mean)
    # s.to_csv('output_' + param1 + '.csv')
    save_list.extend(img_mean)

    # #サンプリング周波数
    # fs = 60

    # end_time = round(len(img_mean)/fs)

    # time = np.arange(0 , end_time , end_time/len(img_mean))
    # # plt.plot(time, img_mean)
    # # plt.xlabel("time(s)",size=15)
    # # plt.show()

s = pd.Series(save_list)
s.to_csv('output_merge1.csv')
