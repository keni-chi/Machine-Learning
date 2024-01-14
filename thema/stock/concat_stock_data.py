import glob
import pandas as pd
import os
import datetime as dt


def concat_data():
    path_list = glob.glob('./dataraw/*.csv')
    path_diff_list = glob.glob('./data_20230401_diff/*.csv')
    for path_diff in path_diff_list:
        file_diff = path_diff.split('\\')[1]
        for path in path_list:
            file_org = path.split('\\')[1]
            if file_diff != file_org:
                continue
            # code
            stock_code = path.split('\\')[1].split('.')[0]
            df_org = pd.read_csv(path)
            df_diff = pd.read_csv(path_diff)

            if int(stock_code.split('_')[1]) <= 9000:
                continue
            if len(df_org)==0:
                continue
            elif len(df_diff)!=0:
                df = pd.concat(
                    [df_org, df_diff],
                    axis=0,
                    ignore_index=True
                )
                df = df.drop_duplicates().sort_values('Date').reset_index(drop=True)
            df.to_csv( os.path.dirname(__file__) + '/data_20230401/'+ stock_code + '.csv')


def main():
    concat_data()


if __name__ == '__main__':
    main()