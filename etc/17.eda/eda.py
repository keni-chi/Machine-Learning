import pandas as pd
import numpy
import os
from ydata_profiling import ProfileReport
import sweetviz as sv
from autoviz.AutoViz_Class import AutoViz_Class


class EDA:
    def __init__(self):
        self.target = 'Time'
        self.df_train = pd.read_csv('./data/input/000.csv', index_col=0)
        self.df_test = pd.read_csv('./data/input/001.csv', index_col=0).drop([self.target], axis=1)

    def make_dir(self):
        # フォルダ作成
        dir1 = './data/output/eda'
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        dir1 = './data/output/eda/yp'
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        dir1 = './data/output/eda/sweetviz'
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        dir1 = './data/output/eda/autoviz'
        if not os.path.exists(dir1):
            os.makedirs(dir1)

    def yp(self):
        # 出力
        profile = ProfileReport(self.df_train, title='ydata_profiling Report')
        profile.to_file('./data/output/eda/yp/yp.html')

    def sweetviz(self):
        my_report = sv.compare([self.df_train, 'Train'], [self.df_test, 'Test'], self.target)
        my_report.show_html('./data/output/eda/sweetviz/sweetviz.html')

    def autoviz(self):
        AV = AutoViz_Class()
        AV.AutoViz(
            '',
            depVar=self.target,
            dfte=self.df_train,
            header=0,
            verbose=1, 
            chart_format='html',
            save_plot_dir='./data/output/eda/autoviz'
        )

    def run(self):
        self.make_dir()
        self.yp()
        self.sweetviz()
        self.autoviz()


if __name__ == '__main__':
    eda = EDA()
    eda.run()
