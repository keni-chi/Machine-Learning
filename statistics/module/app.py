import pandas as pd
import statistic


def main():
    df = pd.read_csv('./input.csv')
    stat = statistic.StatisticalTests()
    df_num = stat.get_df_cols_num(df)

    # 基本情報
    stat.basic_info(df)

    # 信頼区間
    stat.t_interval(df_num)

    # 正規性の検定
    stat.shapiro(df_num)

    # 等分散性の検定
    stat.levene(df_num['x1'], df_num['x2'])
    stat.levene(df_num['x1'], df_num['x5'])

    # 対応ありt検定
    stat.ttest_rel(df_num['x2'], df_num['x1'])
    stat.ttest_rel(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性あり)t検定
    stat.ttest_ind_equal_var_true(df_num['x2'], df_num['x1'])
    stat.ttest_ind_equal_var_true(df_num['x1'], df_num['x5'])

    # 対応なし(2群間に等分散性あり)t検定
    stat.ttest_ind_equal_var_false(df_num['x2'], df_num['x1'])
    stat.ttest_ind_equal_var_false(df_num['x1'], df_num['x5'])

    # 適合度の検定
    # df_sample = df_num.drop('x5', axis=1)
    stat.chisquare(df_num['x1'], df_num['x2'])
    stat.chisquare(df_num['x1'], df_num['x5'])

    # 独立性の検定
    # データサンプル
    df1 = pd.DataFrame([[30, 70], [20, 80]])
    df2 = pd.DataFrame([[30, 200, 200], [15, 100, 400]])
    df3 = pd.DataFrame([[15, 100, 400], [15, 100, 400], [15, 100, 400]])
    # 検定実施
    stat.chi2_contingency(df1)
    stat.chi2_contingency(df2)
    stat.chi2_contingency(df3)

    # 相関係数の検定
    stat.pearsonr(df_num['x1'], df_num['x2'])
    stat.pearsonr(df_num['x1'], df_num['x5'])


if __name__ == '__main__':
    main()
