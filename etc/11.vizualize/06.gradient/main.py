from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

n=100
x = np.linspace(0, 2*np.pi*5, n)
y = np.sin(x) + 2*np.sin(x*4) + 6
df = pd.DataFrame({'x': x, 'y':y})
print(df)
df.plot()
plt.show()


dx = 1
df['d1'] = np.gradient(df['y'], dx)
df['d2'] = np.gradient(df['d1'], dx)
df['y'] = df['y'] * 0.1
df2 = df[['y', 'd1', 'd2']]
print(df2)
df2.plot()
plt.show()


from scipy import signal

#order：int型で指定。次の極小値の判定範囲。最小値＝1
maxid = signal.argrelmin(np.array(df['d2']), order=1)
print(maxid)

x = np.array(df['x'])
d2 = np.array(df['d2'])

plt.plot(x, d2)
plt.plot(x[maxid[0]], d2[maxid[0]], "o")
plt.show()
plt.close()

y = np.array(df['y'])
plt.plot(x, y)
plt.plot(x[maxid[0]], y[maxid[0]], "o")
plt.show()
plt.close()


print('----生波形から極大値を出す場合---')
maxid = signal.argrelmax(y, order=1)
y = np.array(df['y'])
plt.plot(x, y)
plt.plot(x[maxid[0]], y[maxid[0]], "o")
plt.show()
