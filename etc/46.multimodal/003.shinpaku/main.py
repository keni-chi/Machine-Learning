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


#フレーム分割
def frame_split(video_file='./image_wave.wmv', image_dir='./image_wave/',
                   image_file='image_wave-%s.png'):
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    i = 0
    j = 0
    id = 0

    cap = cv2.VideoCapture(video_file)
    while (cap.isOpened()):
        flag, frame = cap.read()  # Capture frame-by-frame
        if flag == False:  
            break
        if i == 100:
            j += 1
            i = 0
            os.mkdir(conf1 + str(j))

        cv2.imwrite(conf1 + str(j) + '/image_' + str(id).zfill(6) + '.png',
                    frame)  
        # cv2.imwrite(image_dir + image_file % str(i).zfill(6),
        #             frame)  
        print('Save', image_dir + image_file % str(i).zfill(6))
        i += 1
        id += 1

    cap.release()

# frame_split("IMG_5652.MOV")
# frame_split("IMG_5666_myaku_midori.MOV")
frame_split(conf1 + ".MOV")

