import get_stock_yahoo
import get_stock_bs
import cluster_kmeans_day
import simple_regression
import simple_regression_plt
import static_month
import simulate_main

# データ取得
print('---get_stock_yahoo---')
get_stock_yahoo.main()
# print('---get_stock_bs---')
# get_stock_bs.main()

# データ整形・可視化
print('---cluster_kmeans_day---')
cluster_kmeans_day.main()
print('---simple_regression---')
simple_regression.main()
# print('---simple_regression_plt---')
# simple_regression_plt.main()
print('---static_month---')
static_month.main()

# 過去データでの損益シミュレーション
print('---simulate_main---')
simulate_main.main()
