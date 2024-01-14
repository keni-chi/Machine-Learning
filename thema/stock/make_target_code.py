import glob
import pandas as pd
import os
import datetime as dt


def main():
    df = pd.read_csv('data_j.csv', encoding='shift_jis')
    df = df[(df['市場・商品区分']=='プライム（内国株式）')|(df['市場・商品区分']=='スタンダード（内国株式）')|(df['市場・商品区分']=='グロース（内国株式）')]
    print('母数')
    print(len(df))

    df = pd.read_csv('dataset/data_j_extract.csv', encoding='shift_jis')
    df = df[(df['市場・商品区分']=='プライム（内国株式）')|(df['市場・商品区分']=='スタンダード（内国株式）')|(df['市場・商品区分']=='グロース（内国株式）')]
    print('make_month_dataの処理後')
    print(len(df))



if __name__ == '__main__':
    main()