import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
N = 32 # データ数
n = np.arange(N)
freq = 3 # 周期
f = np.sin(freq * 2 * np.pi * (n/N)) # freq=3周期分

# グラフ表示
plt.figure(figsize=(8, 4))
plt.xlabel('n')
plt.ylabel('Signal')
plt.plot(f)
plt.show()

F = np.fft.fft(f) # 高速フーリエ変換(FFT)

F_abs = np.abs(F)
plt.plot(F_abs)
plt.show()

