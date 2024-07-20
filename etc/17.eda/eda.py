# EDA
target = 'target'

#########################
# # pip install ydata-profiling
# import pandas as pd
# from ydata_profiling import ProfileReport
# data_train = pd.read_csv('./train.csv')
# profile = ProfileReport(data_train, title="Profiling Report")
# # profile.to_notebook_iframe()
# profile.to_file("yp.html")

# #########################
# pip install sweetviz
# pip install numpy==1.26.4
# import sweetviz as sv
# import pandas as pd
# import numpy
# train = pd.read_csv('./train.csv')
# test = pd.read_csv('./test.csv')
# my_report = sv.compare([train, "Train"], [test, "Test"], target)
# # my_report = sv.analyze(train) # trainデータ単体で分析する場合
# my_report.show_html("sweetviz.html")

#########################
# pip install autoviz
# pip install IPython
# pip install jupyter
# 役立つ：相関係数、カテゴリ毎の目的変数カテゴリでの積み上げ棒グラフ
# from autoviz.AutoViz_Class import AutoViz_Class
# import pandas as pd
# df = pd.read_csv('./train.csv')
# AV = AutoViz_Class()
# dft = AV.AutoViz("",                # csvのファイルパスを指定、今回DataFrameデータを既に読み込んだため、空文字""を指定
#                  depVar=target,   # 列名"target"を目的変数とする。
#                  dfte=df,    # dfteにはDataFrameデータを指定
#                  header=0,          # ヘッダー行を指定 
#                  verbose=1,         # 詳細情報を表示      
#                  chart_format='html'
#                  )
#########################
# ペアプロットはinteractがよい
# import numpy as np
# import pandas as pd
# from ipywidgets import interact, Select
# import matplotlib.pyplot as plt
# %matplotlib inline

# data = pd.read_csv('./train.csv')
# def show_plot(col1, col2):
#     plt.figure(figsize=(6,6))
#     plt.scatter(data[col1], data[col2], c=data[target])
#     plt.xlabel('')
#     plt.ylabel('')
#     plt.show()
# w1 = Select(description='X軸:', options=data.columns, rows=4,)
# w2 = Select(description='Y軸:', options=data.columns, rows=4,)
# interact(show_plot, col1=w1, col2=w2)

