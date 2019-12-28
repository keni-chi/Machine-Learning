import pandas as pd
from statistic import StatisticalTests as Stat

def main():
    df = pd.read_csv('./input.csv')
    df_num = Stat.get_df_cols_num(df)

    # 基本情報
    Stat.basic_info(df)

    # 信頼区間
    Stat.t_interval(df_num)

    # 正規性の検定
    Stat.shapiro(df_num)

    # 等分散性の検定
    Stat.levene(df_num['x1'], df_num['x2'])
    Stat.levene(df_num['x1'], df_num['x5'])

    # 対応ありt検定
    Stat.ttest_rel(df_num['x2'], df_num['x1'])
    Stat.ttest_rel(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性あり)t検定
    Stat.ttest_ind_equal_var_true(df_num['x2'], df_num['x1'])
    Stat.ttest_ind_equal_var_true(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性なし)t検定
    Stat.ttest_ind_equal_var_false(df_num['x2'], df_num['x1'])
    Stat.ttest_ind_equal_var_false(df_num['x1'], df_num['x5'])

    # 適合度の検定
    # df_sample = df_num.drop('x5', axis=1)
    Stat.chisquare(df_num['x1'], df_num['x2'])
    Stat.chisquare(df_num['x1'], df_num['x5'])

    # 独立性の検定
    # データサンプル
    df1 = pd.DataFrame([[30, 70], [20, 80]])
    df2 = pd.DataFrame([[30, 200, 200], [15, 100, 400]])
    df3 = pd.DataFrame([[15, 100, 400], [15, 100, 400], [15, 100, 400]])
    # 検定実施
    Stat.chi2_contingency(df1)
    Stat.chi2_contingency(df2)
    Stat.chi2_contingency(df3)

    # 相関係数の検定
    Stat.pearsonr(df_num['x1'], df_num['x2'])
    Stat.pearsonr(df_num['x1'], df_num['x5'])


if __name__ == '__main__':
    main()
