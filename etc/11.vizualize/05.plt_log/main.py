from matplotlib import pyplot as plt
import pandas as pd


df = pd.read_csv('input.csv')
print(df)

plt.xlim(0.2,10)
plt.ylim(10,90)
plt.scatter(df['a'],df['b'],marker='o')
plt.xscale('log')
plt.grid()

plt.hlines(57,0.2,10,color="black")
plt.hlines(42,0.2,10,color="black")
plt.hlines(37,0.2,10,color="black")

plt.vlines(0.8,0,100,color="black")
plt.vlines(2.0,0,100,color="black")
plt.vlines(5.0,0,100,color="black")


plt.show()

