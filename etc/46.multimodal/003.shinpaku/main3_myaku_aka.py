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
foldernum = 14

# for param1 in p1_list:
def myaku_numeric(rgb):
    save_list = []
    i = 0
    for param1 in range(1, foldernum):
        print('param1: ', param1)

        #画像ファイルを格納，時系列にソート
        files = glob.glob(conf1 + str(param1)  + "/*.png")
        files.sort()

        #画像を読み込み，green成分を抽出
        images = [cv2.imread(files[i]) for i in range(len(files))]
        images_blue = [pd.DataFrame(images[j][:,:,rgb]) for j in range(len(images))]
        # print(images_green[0])

        # 1920*1080
        #parameter
        in1 = 100
        in2 = 1800
        co1 = 100
        co2 = 900

        #メディアンフィルタによる平滑化
        images_median_blue = [cv2.medianBlur(images_blue[i].iloc[ in1 : in2 , co1 :co2 ].values,ksize=5)  for i in range(len(images_blue))]

        #平均値を算出
        img_mean_blue = [images_median_blue[i].mean()  for i in range(len(images_median_blue))]

        save_list.extend(img_mean_blue)

        i +=1
    return save_list

rgb = 0  #blue
save_blue_list = myaku_numeric(rgb)

rgb = 1  #green
save_green_list = myaku_numeric(rgb)

rgb = 2  #red
save_red_list = myaku_numeric(rgb)

df = pd.DataFrame({'blue': save_blue_list, 'green': save_green_list, 'red': save_red_list})
df.to_csv('IMG_5669_myaku_aka_numeric/' + conf1 + '.csv')
