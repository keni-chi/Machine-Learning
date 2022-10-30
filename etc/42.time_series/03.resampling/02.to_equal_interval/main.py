from re import T
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt
import pandas as pd

# ここからサンプルとなる波形の作成-------------
# スムース関数
def smooth(x):
    a = 30
    y = np.tanh(x) / (1 + a * np.exp(- x))
    return y

A = 1    # 振幅
t0 = 0   # 初期時間[s]
tf = 10  # 終了時間[s]
dt = 0.2 # 時間刻み[s]
f = 1    # 周波数[Hz}
t = np.arange(t0, tf + dt, dt)  # 時間軸

# 滑らかに振幅増加する正弦波
y = smooth(t) * A * np.sin(2 * np.pi * f * t)
# ここまでサンプルとなる波形の作成-------------
print('t:', t)
print('y:', y)

# 補間関数fを作成
f = interpolate.interp1d(t, y, kind='linear')

# 補間した結果からリサンプリング波形を生成
num = 10000
t_resample = np.linspace(t0, tf, num)
y_resample = f(t_resample)              # f(t)
print('t_resample:', len(t_resample), t_resample)
print('y_resample:', len(y_resample), y_resample)


# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

# 軸のラベルを設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('y')

# 軸の範囲設定
ax1.set_xticks(np.arange(0, 20, 1))
ax1.set_yticks(np.arange(-2, 2, 0.5))
ax1.set_xlim(0, 10)
ax1.set_ylim(-1.5, 1.5)

# データプロット
ax1.scatter(t_resample, y_resample, label="resample", s=5)
ax1.scatter(t, y, label="original")

# レイアウトと凡例
fig.tight_layout()
plt.legend(loc='upper left')

# グラフを表示する。
plt.show()
plt.close()

print('-------------------間隔がバラバラ----------------------')

# ここからサンプルとなる波形の作成-------------
# スムース関数
def smooth(x):
    a = 30
    y = np.tanh(x) / (1 + a * np.exp(- x))
    return y

A = 1    # 振幅
t0 = 0   # 初期時間[s]
tf = 10  # 終了時間[s]
dt = 0.2 # 時間刻み[s]
f = 1    # 周波数[Hz}
t = np.arange(t0, tf + dt, dt)  # 時間軸

# 滑らかに振幅増加する正弦波
y = smooth(t) * A * np.sin(2 * np.pi * f * t)

# データを歯抜けにする
t = np.delete(t, 3)
y = np.delete(y, 3)
t = np.delete(t, 7)
y = np.delete(y, 7)

# seriesへ変換
t = pd.Series(t)
y = pd.Series(y)

# ここまでサンプルとなる波形の作成-------------
print('t:', t)
print('y:', y)

# 補間関数fを作成
f = interpolate.interp1d(t, y, kind='linear')

# 補間した結果からリサンプリング波形を生成
num = 10000
t_resample = np.linspace(t0, tf, num)
y_resample = f(t_resample)              # f(t)
print('t_resample:', len(t_resample), t_resample)
print('y_resample:', len(y_resample), y_resample)


# ここからグラフ描画
# フォントの種類とサイズを設定する。
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'

# 目盛を内側にする。
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# グラフの上下左右に目盛線を付ける。
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')

# 軸のラベルを設定する。
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('y')

# 軸の範囲設定
ax1.set_xticks(np.arange(0, 20, 1))
ax1.set_yticks(np.arange(-2, 2, 0.5))
ax1.set_xlim(0, 10)
ax1.set_ylim(-1.5, 1.5)

# データプロット
ax1.scatter(t_resample, y_resample, label="resample", s=5)
ax1.scatter(t, y, label="original")

# レイアウトと凡例
fig.tight_layout()
plt.legend(loc='upper left')

# グラフを表示する。
plt.show()
plt.close()
