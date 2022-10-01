import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit 

x = np.linspace(0, 40*(2*np.pi), 500)
y = np.sin(x) + 2*np.sin(x/4)
df = pd.DataFrame({'x': x, 'y': y})
print(df.head())

plt.plot(x, y)


def func(X, *params):
    Y = np.zeros_like(X)
    for i, param in enumerate(params):
        Y = Y + np.array(param * X ** i)
    return Y


popt, pcov = curve_fit(func, x, y, p0=[0, 0, 0, 0, 0, 0, 0, 0, 0]) 
print(popt)

y_pred = func(x, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8])
print(y_pred)
print(len(y_pred))
df['y_pred'] = y_pred
print(df.head())
plt.plot(x, df['y_pred'])


df['y_roll'] = df['y'].rolling(15, center=True).mean()
plt.plot(x, df['y_roll'])



plt.show()
