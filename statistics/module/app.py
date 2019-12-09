import pandas as pd
import statistic


def main():
    df = pd.read_csv('./input.csv')
    s = statistic.StatisticalTests()
    df_num = s.get_df_cols_num(df)

    # 基本情報
    s.basic_info(df)

    # 信頼区間
    s.t_interval(df_num)

    # 正規性の検定
    s.shapiro(df_num)

    # 等分散性の検定
    s.levene(df_num['x1'], df_num['x2'])
    s.levene(df_num['x1'], df_num['x5'])

    # 対応ありt検定
    s.ttest_rel(df_num['x2'], df_num['x1'])
    s.ttest_rel(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性あり)t検定
    s.ttest_ind_equal_var_true(df_num['x2'], df_num['x1'])
    s.ttest_ind_equal_var_true(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性あり)t検定
    s.ttest_ind_equal_var_false(df_num['x2'], df_num['x1'])
    s.ttest_ind_equal_var_false(df_num['x1'], df_num['x5'])

    # 適合度の検定
    # df_sample = df_num.drop('x5', axis=1)
    s.chisquare(df_num['x1'], df_num['x2'])
    s.chisquare(df_num['x1'], df_num['x5'])

    # 独立性の検定
    # データサンプル
    df1 = pd.DataFrame([[30, 70], [20, 80]])
    df2 = pd.DataFrame([[30, 200, 200], [15, 100, 400]])
    df3 = pd.DataFrame([[15, 100, 400], [15, 100, 400], [15, 100, 400]])
    # 検定実施
    s.chi2_contingency(df1)
    s.chi2_contingency(df2)
    s.chi2_contingency(df3)

    # 相関係数の検定
    s.pearsonr(df_num['x1'], df_num['x2'])
    s.pearsonr(df_num['x1'], df_num['x5'])


if __name__ == '__main__':
    main()
