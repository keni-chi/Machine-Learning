import pandas as pd
import scipy.stats as st
import math
import numpy as np
# import matplotlib.pyplot as plt


class StatisticalTests():
    def __init__(self):
        pass

    def basic_info(self, df):
        print('基本統計量------------------start')
        print('df.head(3)-------------')
        print(df.head(3))
        print('df.dtypes-------------')
        print(df.dtypes)
        print('df.describe(include=\'all\')-------------')
        print(df.describe(include='all'))

    def get_df_cols_num(self, df):
        dt = ['int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32',
              'uint64', 'float16', 'float32', 'float64', 'float128']
        df_con = pd.DataFrame()

        for d in dt:
            if df_con.empty:
                df_con = df.select_dtypes(include=d)
            else:
                temp = df.select_dtypes(include=d)
                df_con = pd.concat([df_con, temp], axis=1)

        return df_con

    def t_interval(self, df):
        print('母平均の95%信頼区間-------------------start')
        for column_name, s in df.iteritems():
            u2 = s.var(ddof=1)  # 母集団の分散推定値（不偏分散）
            m = s.mean()  # 標本平均
            n = len(s)-1  # 自由度
            se = math.sqrt(u2/len(s))  # 標準誤差

            ci1, ci2 = st.t.interval(alpha=0.95, loc=m, scale=se, df=n)
            print(f'カラム名 = {column_name} // 母平均の95%信頼区間CI = \
                  [{ci1:.2f} , {ci2:.2f}] // 標本平均[{m}]')

    def shapiro(self, df):
        print('シャピロ・ウィルク検定(データの正規性の統計検定)------------------start')
        for column_name, s in df.iteritems():
            _, p = st.shapiro(s)
            if p >= 0.05:
                print(f'カラム名 = {column_name} // p値 = {p:.3f} \
                      // 検定結果: 帰無仮説を採択して、正規性あり')
            else:
                print(f'カラム名 = {column_name} // p値 = {p:.3f} \
                      // 検定結果: 帰無仮説を棄却して、正規性なし')

    def ttest_ind(self, xa, xb):
        print('2群間: 対応なしt検定-------------------start')
        # 2つの標本の平均値に有意差がないことを帰無仮説とする
        # 対応なしでは、Ａさん、Ｂさんのように薬の投与前後で同じ人を調べない
        t, p = st.ttest_ind(xa, xb, equal_var=True)
        if np.sign(t) == -1:
            a = xa
            xa = xb
            xb = a

        t, p = st.ttest_ind(xa, xb, equal_var=True)
        mu = abs(xa.mean()-xb.mean())
        se = mu/t
        df = len(xa)+len(xb)-2
        ci1, ci2 = st.t.interval(alpha=0.95, loc=mu, scale=se, df=df)
        if p >= 0.05:
            print(f'p値={p:.3f} // t値 = {t:.2f}')
            print(f'// 平均値の差 = {mu:.2f} // 差の標準誤差 = {se:.2f}')
            print(f'// 平均値の差の95%信頼区間CI = [{ci1:.2f} , {ci2:.2f}]')
            print('// 検定結果: 帰無仮説を採択して、2つの標本の平均値に有意差なし')
        else:
            print(f'p値={p:.3f} // t値 = {t:.2f}')
            print(f'// 平均値の差 = {mu:.2f} // 差の標準誤差 = {se:.2f}')
            print(f'// 平均値の差の95%信頼区間CI = [{ci1:.2f} , {ci2:.2f}]')
            print(f'// 検定結果: 帰無仮説を棄却して、2つの標本の平均値に有意差あり')

    def levene(self, xa, xb):
        print('2群間: 母平均の95%ルビーン検定による等分散性のチェック-------------------start')
        _, p = st.levene(xa, xb, center='mean')
        if p >= 0.05:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、2つの標本には等分散性あり')
        else:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、2つの標本には等分散性なし')

    def chi2_contingency(self, df):
        print('独立性の検定-------------------start')
        # Usage)
        #       発ガン人数	非発ガン人数
        # 喫煙群	     30	          70
        # 非喫煙群	    20	         80
        # print(st.chi2_contingency(x))
        p = st.chi2_contingency(df.values)[1]
        if p >= 0.05:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、2つの変数は独立していないと結論付けられない。')
        else:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、2つの変数は独立していないと結論付けられる。')

    def chisquare(self, sample, answer):
        print('適合度の検定-------------------start')
        # 対立仮説：得られたデータは理論上の分布に適合しない。
        sample = sample.tolist()
        answer = answer.tolist()

        p = st.chisquare(sample, f_exp=answer)[1]
        if p >= 0.05:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を採択して、理論上の分布に適合しないと結論づけられない。')
        else:
            print(f'p値 = {p:.3f} // 検定結果: 帰無仮説を棄却して、理論上の分布に適合しないと結論づけられる。')


def main():
    df = pd.read_csv('./input.csv')
    s = StatisticalTests()
    df_num = s.get_df_cols_num(df)

    # 基本情報
    s.basic_info(df)

    # 信頼区間
    s.t_interval(df_num)

    # 検定
    s.shapiro(df_num)
    s.levene(df_num['x1'], df_num['x2'])
    s.levene(df_num['x1'], df_num['x5'])
    s.ttest_ind(df_num['x2'], df_num['x1'])
    s.ttest_ind(df_num['x1'], df_num['x5'])

    # 検定（適合度）
    df_sample = df_num.drop('x5', axis=1)
    s.chisquare(df_sample['x1'], df_num['x2'])
    s.chisquare(df_sample['x1'], df_num['x5'])

    # 検定（独立性）
    # データサンプル
    df1 = pd.DataFrame([[30, 70], [20, 80]])
    df2 = pd.DataFrame([[30, 200, 200], [15, 100, 400]])
    df3 = pd.DataFrame([[15, 100, 400], [15, 100, 400], [15, 100, 400]])
    # 検定実施
    s.chi2_contingency(df1)
    s.chi2_contingency(df2)
    s.chi2_contingency(df3)


if __name__ == '__main__':
    main()
