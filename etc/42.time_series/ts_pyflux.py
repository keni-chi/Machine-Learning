import numpy as np
import pandas as pd
import pyflux as pf
from datetime import datetime
import matplotlib.pyplot as plt


def read_data():
    data = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/sunspot.year.csv')
    data.index = data['time'].values

    plt.figure(figsize=(15, 5))
    plt.plot(data.index, data['sunspot.year'])
    plt.ylabel('Sunspots')
    plt.title('Yearly Sunspot Data')
    plt.show()


def main():
    read_data()



if __name__ == '__main__':
    print('main---start')
    main()

