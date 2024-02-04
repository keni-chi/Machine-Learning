import usa_get_stock_yahoo
# import get_stock_bs
import usa_cluster_kmeans_day
import usa_simple_regression
# import usa_simple_regression_plt
import usa_static_month
import usa_simulate_main

# データ取得
print('---usa_get_stock_yahoo---')
# usa_get_stock_yahoo.main()
# print('---get_stock_bs---')
# get_stock_bs.main()

# データ整形・可視化
print('---usa_cluster_kmeans_day---')
usa_cluster_kmeans_day.main()
print('---usa_simple_regression---')
usa_simple_regression.main()
# print('---simple_regression_plt---')
# simple_regression_plt.main()
print('---usa_static_month---')
usa_static_month.main()

# # 過去データでの損益シミュレーション
# print('---usa_simulate_main---')
# usa_simulate_main.main()
