import glob
import pandas as pd
import os
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error as mape


def filter_close_v():
    path_list = glob.glob('./data-yahoo-20240319/*.csv')

    code_list = []
    close_list = []
    volume_list = []
    one_day_change_ratio_list = []
    coef_6m_list = []
    coef_1m_list = []
    coef_2w_list = []
    mape_list = []

    for path in path_list:
        # codeを抽出
        code = int(path.split('_')[1].split('.')[0])
        print('------')
        print(code)

        # #debug
        # if code>2500:
        #     break

        # read
        df = pd.read_csv(path)        

        # close値を取得
        c_list = df['Close'].tolist()
        if len(c_list) == 0:
            continue
        close_v = c_list[-1]

        # 出来高
        df_6month = df.tail(20*6)
        volume_mean = int(df_6month['Volume'].mean())

        # 欠損がないことを確認
        x = df_6month.isnull().values.sum()
        if x!=0:
            continue

        # 一日の変動率
        df_6month = df_6month.reset_index(drop=True)
        df_6month['h-l'] = (df_6month['High'] - df_6month['Low'])/df_6month['Low']
        one_day_change_ratio = df_6month['h-l'].mean()

        # coef
        df_6month['close_ratio'] = df_6month['Close']/close_v
        # 6m------
        X = df_6month[['close_ratio']]
        y = df_6month.index.tolist()
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a_6m = model_lr.coef_
        # mape
        y_pred = model_lr.predict(X)
        mape_score = mape(y, y_pred)
        # 1m------
        df_1m = df_6month.copy()
        df_1m = df_1m.tail(20)
        X = df_1m[['close_ratio']]
        y = df_1m.index.tolist()
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a_1m = model_lr.coef_
        # 2w------
        df_2w = df_6month.copy()
        df_2w = df_2w.tail(10)
        X = df_2w[['close_ratio']]
        y = df_2w.index.tolist()
        model_lr = LinearRegression()
        model_lr.fit(X, y)
        a_2w = model_lr.coef_

        # append
        code_list.append(code)
        close_list.append(close_v)
        volume_list.append(volume_mean)
        one_day_change_ratio_list.append(one_day_change_ratio)
        coef_6m_list.append(a_6m[0])
        coef_1m_list.append(a_1m[0])
        coef_2w_list.append(a_2w[0])
        mape_list.append(mape_score)

    df = pd.DataFrame(data={
        'コード': code_list,
        'close': close_list,
        'volume': volume_list,
        'one_day_change_ratio': one_day_change_ratio_list,
        'coef_6m': coef_6m_list,
        'coef_1m': coef_1m_list,
        'coef_2w': coef_2w_list,
        'mape': mape_list
    })

    df_j = pd.read_csv('./data_j_prime.csv', encoding='shift-jis')
    df = pd.merge(df, df_j, on='コード', how='left')

    # 1次フィルタ------------------------------------------------------------------
    # 全結果
    print('すべて: ', len(df))
    # 固定除外コード
    for code in [6367, 7011, 7105, 7211]:
        df = df[df['コード']!=code]
    print('固定除外コード: ', len(df))
    # 市場
    df = df[df['市場・商品区分']=='プライム（内国株式）']
    print('市場: ', len(df))
    # 規模区分
    df = df[(df['規模区分']=='TOPIX Large70')|(df['規模区分']=='TOPIX Mid400')|(df['規模区分']=='TOPIX Small 1')]
    print('規模区分: ', len(df))
    # 出来高100万以上
    df = df[df['volume']>=1000000]
    print('出来高100万以上: ', len(df))

    # 2次フィルタ------------------------------------------------------------------
    # close10~30万-----------------
    df_10 = df[(df['close']>=1000)&(df['close']<3000)]
    print('close10~30万: ', len(df_10))
    output_result(df_10, 'from10to30')

    # close30~50万-----------------
    df_30 = df[(df['close']>=3000)&(df['close']<5000)]
    print('close30~50万: ', len(df_30))
    output_result(df_30, 'from30to50')

    # close30~50万-----------------
    df_50 = df[(df['close']>=5000)&(df['close']<10000)]
    print('close50~100万: ', len(df_50))
    output_result(df_50, 'from50to100')


    # print('coef_6m>0---------------------')
    # df_6m = df[df['coef_6m']>=0]
    # print('coef_6m>0: ', len(df_6m))
    # # one_day_change_ratioの大きい順
    # df_6m = df_6m.sort_values('one_day_change_ratio', ascending=False)
    # # 上位40銘柄に絞る
    # df_6m = df_6m.head(40)
    # print('上位40銘柄に絞る: ', len(df_6m))
    # # 出力
    # df_6m.to_csv('./d_select_code/df_target_code(6m).csv', encoding='shift-jis')

    # print('coef_1m>0---------------------')
    # df_1m = df[df['coef_1m']>=0]
    # print('coef_1m>0: ', len(df_1m))
    # # one_day_change_ratioの大きい順
    # df_1m = df_1m.sort_values('one_day_change_ratio', ascending=False)
    # # 上位40銘柄に絞る
    # df_1m = df_1m.head(40)
    # print('上位40銘柄に絞る: ', len(df_1m))
    # # 出力
    # df_1m.to_csv('./d_select_code/df_target_code(1m).csv', encoding='shift-jis')

    # print('coef_2w>0---------------------')
    # df_2w = df[df['coef_2w']>=0]
    # print('coef_2w>0: ', len(df_2w))
    # # one_day_change_ratioの大きい順
    # df_2w = df_2w.sort_values('one_day_change_ratio', ascending=False)
    # # 上位40銘柄に絞る
    # df_2w = df_2w.head(40)
    # print('上位40銘柄に絞る: ', len(df_2w))
    # # 出力
    # df_2w.to_csv('./d_select_code/df_target_code(2w).csv', encoding='shift-jis')


def output_result(df, info_str):
    print('coef_6m,1m,2w>0---------------------')
    df_all = df[(df['coef_6m']>=0)&(df['coef_1m']>=0)&(df['coef_2w']>=0)]
    print('coef_6m,1m,2w>0: ', len(df_all))
    # one_day_change_ratioの大きい順
    df_all = df_all.sort_values('one_day_change_ratio', ascending=False)
    # 上位40銘柄に絞る
    df_all = df_all.head(40)
    print('上位40銘柄に絞る: ', len(df_all))
    # 出力
    df_all.to_csv(f'./d_select_code/df_target_code_{info_str}.csv', encoding='shift-jis')


def main():
    print('main---start')
    filter_close_v()
    print('main---end')


if __name__ == '__main__':
    main()