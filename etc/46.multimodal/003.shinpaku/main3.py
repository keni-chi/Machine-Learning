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

conf1 = 'IMG_5669_myaku_aka'


# p1_list = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', '1100', '1200', '1300', '1400', '1500']
save_list = []
i = 0
foldernum = 14

# for param1 in p1_list:
for param1 in range(1, foldernum):

    #画像ファイルを格納，時系列にソート
    files = glob.glob(conf1 + str(param1)  + "/*.png")
    files.sort()

    #画像を読み込み，green成分を抽出
    images = [cv2.imread(files[i]) for i in range(len(files))]
    # images_green = [pd.DataFrame(images[j][:,:,1]) for j in range(len(images))]
    images_green = [pd.DataFrame(images[j][:,:,2]) for j in range(len(images))]   # red
    print(images_green[0])

    # 1920*1080
    #parameter
    # in1 = 100
    # in2 = 900
    # co1 = 450
    # co2 = 1000

    in1 = 100
    in2 = 1800
    co1 = 100
    co2 = 900


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
    i +=1

s = pd.Series(save_list)
s.to_csv(conf1 + '.csv')
