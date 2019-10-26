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
    print('2群間: 対応なしt検定(1A)-------------------start')
    # 2つの標本の平均値に有意差がないことを帰無仮説とする
    t, p = st.ttest_ind(xa, xb, equal_var=True)
    MU = abs(xa.mean()-xb.mean())
    SE =  MU/t
    DF = len(xa)+len(xb)-2
    CI1,CI2 = st.t.interval( alpha=0.95, loc=MU, scale=SE, df=DF )
    if p >= 0.05:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、2つの標本の平均値に有意差なし')
    else:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、2つの標本の平均値に有意差あり')
    print(f't値 = {t:.2f}')
    print(f'平均値の差   = {MU:.2f}')
    print(f'差の標準誤差 = {SE:.2f}')
    print(f'平均値の差の95%信頼区間CI = [{CI1:.2f} , {CI2:.2f}]')
    print('2群間: 対応なしt検定(1A)-------------------end')
    

def create_std_data():
    print('データ生成-------------------start')
    a = (np.random.normal(80,5,size=40)).astype(np.int64).tolist()
    print(a)
    xa = pd.Series(a).hist()
    plt.show(xa)
    print('データ生成-------------------end')


def binom():
    print('母比率pの95%信頼区間-------------------start')
    alpha=0.95 # 信頼区間
    n=200      # 試行回数
    p=7/200    # 標本比率(成功回数を試行回数で割ったもの)
    bottom, up = st.binom.interval(alpha=alpha, n=n, p=p, loc=0)
    print('母比率pの95%信頼区間: {:.2f} < p < {:.2f}'.format(bottom/n, up/n))
    print('母比率pの95%信頼区間-------------------end')


def chi2_contingency():
    print('独立性の検定-------------------start')
    # 独立性の検定
    #       発ガン人数	非発ガン人数
    # 喫煙群	     30	          70
    # 非喫煙群	    20	         80
    p = st.chi2_contingency(np.array([[30,70],[20,80]]))[1]
    if p >= 0.05:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、喫煙と発ガンの2つの変数は独立していないと結論付けられない。')
    else:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、喫煙と発ガンの2つの変数は独立していないと結論付けられる。')
    print('独立性の検定-------------------end')


def chisquare():
    print('適合度の検定-------------------start')
    # 対立仮説：得られたデータは理論上の分布に適合しない。
    # p = st.chisquare([8, 12, 8, 12, 8, 12], f_exp=[10, 10, 10, 10, 10, 10])
    p = st.chisquare([9, 10, 10, 10, 10], f_exp=[10, 10, 10, 10, 10])
    print(p)
    print('適合しているほど、P値は1に近く。尚、[0]のstatisticの値は、カイ二乗値を表す。')
    print('----')
    p = st.chisquare([8, 12, 8, 12, 8, 12], f_exp=[10, 10, 10, 10, 10, 10])[1]
    if p >= 0.05:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、得られたデータが理論上の分布に適合しないと結論づけられない。')
    else:
        print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、得られたデータが理論上の分布に適合しないと結論づけられる。')

    print('適合度の検定-------------------end')


def corr():
    print('相関係数の検定-------------------start')
    # 帰無仮説と対立仮説をたてる: 帰無仮説は ρ=0 、つまり母相関 =0 
    # 対立仮説は「 ρ≠0 」、つまり母相関 ≠0
 
    d1 = np.array([6,10,6,10,5,3,5,9,3,3,11,6,11,9,7,5,8,7,7,9])
    d2 = np.array([10,13,8,15,8,6,9,10,7,3,18,14,18,11,12,5,7,12,7,7])

    SampleCorr = st.pearsonr(d1, d2)
    print('相関係数---')
    r = SampleCorr[0]
    print(r)
    print('p値---')
    p = SampleCorr[1]
    print(p)

    if p < 0.05:
        print('棄却する。相関あり。')
    else:
        print('棄却しない。相関なし。')

    print('相関係数の検定-------------------end')


def main():
    xa, xb = read_data()

    basic_info(xa, 'A群')
    basic_info(xb, 'B群')
    basic_diff(xa, xb)
    # plt_hist(xa)
    # plt_hist(xb)
    # plt_multi(xa, xb)
    test_std(xa, 'A群') # 正規性の検定
    test_std(xb, 'B群')
    interval_estimation(xa, 'A群') # 母平均　信頼区間
    interval_estimation(xb, 'B群')
    test_equal_dispersion(xa, xb) # 分散の検定
    test_ave_diff(xa, xb) # 平均の検定
    # create_std_data()

    #　############################
 
    binom() # 母比率の検定
    chi2_contingency() # 独立性の検定
    chisquare() # 適合度の検定

    #　############################

    corr() # 相関係数の検定



if __name__ == '__main__':
    main()
