import numpy as np
import matplotlib.pyplot as plt
 

def Hampel(x, k, thr=3):
    '''
    * Input
        * x       input data
        * k       half window size (full 2*k+1)          
        * thr     threshold (defaut 3), optional
    
    * Output
        * output_x    filtered data
        * output_Idx indices of outliers
    '''
    arraySize = len(x)
    idx = np.arange(arraySize)
    output_x = x.copy()
    output_Idx = np.zeros_like(x)
 
    for i in range(arraySize):
        mask1 = np.where( idx >= (idx[i] - k) ,True, False)
        mask2 = np.where( idx <= (idx[i] + k) ,True, False)
        kernel = np.logical_and(mask1, mask2)
        median = np.median(x[kernel])
        std = 1.4826 * np.median(np.abs(x[kernel] - median))
        print('-----start')
        print("mask1 =", mask1)
        print("mask2 =", mask2)
        print("kernel =", kernel.astype(int))
        print("x[kernel] =", x[kernel])
        print("median =", median)
        print(np.abs(x[kernel] - median))
        print(np.median(np.abs(x[kernel] - median)))
        print("std =", std)
        print('-----end')
        if np.abs(x[i] - median) > thr * std:
            output_Idx[i] = 1
            output_x[i] = median
 
    # return output_x, output_Idx.astype(bool)
    print('******')
    print(output_x)
    print(output_Idx)
    return output_x, output_Idx



# sin波を用意
t = np.arange(0, 2*np.pi, np.pi/36)
x = np.sin(t)
 
# 外れ値を挿入
x[6] = 2
x[16] = -2
x[30] = -1.8
x[42] = 2.5
x[60] = -2.5
 
plt.plot(t, x, marker="o")
plt.title('Input Signal')
plt.xlabel('t')
plt.ylabel('x')
plt.grid()
plt.show()

result = Hampel(x, k=2, thr=3)
# print('Filtered Signal =', result[0])
# print('Index =', result[1])

plt.plot(t, x, marker="o", label = 'Input signal')
plt.plot(t, result[0], linewidth = 2.0,label = 'Filtered signal')
plt.title('Hampel Filter')
plt.xlabel('t')
plt.ylabel('x')
plt.legend()
plt.grid()
plt.show()


