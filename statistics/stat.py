import math
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import numpy as np


def read_data():
    xa = pd.Series( [75, 87, 89, 80, 84, 81, 88, 83, 88, 88, 82, 72, 74, 93, 77, 67, 88, 84, 68, 84, 80, 78, 75, 71, 82, 74, 84, 77, 79, 76, 83, 75, 86, 76, 80, 76, 68, 72, 75, 85])
    xb = pd.Series( [64, 77, 79, 73, 89, 82, 59, 85, 80, 75, 65, 79, 65, 74, 73, 72, 69, 83, 90, 73, 88, 59, 62, 80, 64, 74, 81, 70, 69, 67, 81, 67, 72, 71, 72, 78, 78, 82, 72, 71])
    return xa, xb


def basic_info(x, info):
    print(f'{info}: 基本情報-------------------start')
    print(f'サイズ = {x.size}')
    print(f'平均 = {x.mean():.2f}')
    print(f'標準偏差（不偏標準偏差）= {x.std(ddof=1):.2f}')
    print(f'{info}: 基本情報-------------------end')


def basic_diff(xa, xb):
    print(f'2群間: 基本情報-------------------start')
    print(f'2群の平均の差 = {(abs(xa.mean()-xb.mean())):.2f}')
    print(f'2群間: 基本情報-------------------start')


def plt_hist(x):
    plt.hist(x,bins=9,range=(55,100),color='r')
    plt.show()


def plt_multi(xa, xb):
    # 正規性チェックのためのヒストグラム描画
    fig = plt.figure(dpi=96)
    ax1 = fig.add_subplot(211) 
    ax1.set_xlim(55, 100)
    ax1.set_ylim(0, 15)
    ax1.hist(xa,bins=9,range=(55,100),color='r')
    
    ax2 = fig.add_subplot(212) 
    ax2.set_xlim(55, 100)
    ax2.set_ylim(0, 15)
    ax2.hist(xb,bins=9,range=(55,100),color='b')
    plt.show()
    
    
def test_std(x, info):
    print(f'{info}: シャピロ・ウィルク検定(データの正規性の統計検定)-------------------start')
    _, pa = st.shapiro(x)
    if pa >= 0.05:
        print(f'p値 = {pa:.3f} // 検定結果: 帰無仮説を採択して、正規性あり')
    else:
        print(f'p値 = {pa:.3f} // 検定結果: 帰無仮説を棄却して、正規性なし')
    print(f'{info}: シャピロ・ウィルク検定(データの正規性の統計検定)-------------------end')


def interval_estimation(x, info):
    print(f'{info}: 母平均の95%信頼区間を求める-------------------start')
    u2 = x.var(ddof=1)  # 母集団の分散推定値（不偏分散）
    m = x.mean()        # 標本平均
    DF = len(x)-1       # 自由度
    SE = math.sqrt(u2/len(x)) # 標準誤差

    CI1,CI2 = st.t.interval(alpha=0.95, loc=m, scale=SE, df=DF)
    print(f'標本Aの母平均の95%信頼区間CI = [{CI1:.2f} , {CI2:.2f}] // 標本平均[{m}]')
    print(f'{info}: 母平均の95%信頼区間を求める-------------------end')


def test_equal_dispersion(xa, xb):
    print('2群間: 母平均の95%ルビーン検定による等分散性のチェック-------------------start')
    _, p = st.levene(xa,xb,center='mean')
    print(f'p値 = {p:.3f}')
    if p >= 0.05:
        print('検定結果: 帰無仮説を採択して、2つの標本には等分散性あり')
    else:
        print('検定結果: 帰無仮説を棄却して、2つの標本には等分散性なし')
    print('2群間: 母平均の95%ルビーン検定による等分散性のチェック-------------------end')


def test_ave_diff(xa, xb):
    print('2群間: 対応なしt検定-------------------start')
    # 2つの標本の平均値に有意差がないことを帰無仮説とする
    t, p = st.ttest_ind(xa, xb, equal_var=True)
    MU = abs(xa.mean()-xb.mean())
    SE =  MU/t
    DF = len(xa)+len(xb)-2
    CI1,CI2 = st.t.interval( alpha=0.95, loc=MU, scale=SE, df=DF )
    if p >= 0.05:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、2つの標本の平均値に有意差あり')
    else:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、2つの標本の平均値に有意差なし')
    print(f't値 = {t:.2f}')
    print(f'平均値の差   = {MU:.2f}')
    print(f'差の標準誤差 = {SE:.2f}')
    print(f'平均値の差の95%信頼区間CI = [{CI1:.2f} , {CI2:.2f}]')
    print('2群間: 対応なしt検定-------------------end')
    

def create_std_data():
    print('データ生成-------------------start')
    a = (np.random.normal(80,5,size=40)).astype(np.int64).tolist()
    print(a)
    xa = pd.Series(a).hist()
    plt.show(xa)
    print('データ生成-------------------end')


def main():
    xa, xb = read_data()

    basic_info(xa, 'A群')
    basic_info(xb, 'B群')
    basic_diff(xa, xb)
    # plt_hist(xa)
    # plt_hist(xb)
    plt_multi(xa, xb)
    test_std(xa, 'A群')
    test_std(xb, 'B群')
    interval_estimation(xa, 'A群')
    interval_estimation(xb, 'B群')
    test_equal_dispersion(xa, xb)
    test_ave_diff(xa, xb)
    # create_std_data()


if __name__ == '__main__':
    main()
