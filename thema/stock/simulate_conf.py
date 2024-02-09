import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

RUNDATE = now.strftime('%Y%m%d')
# RUNDATE = '20240119'
LATESTDATE = '20231229'

DATASET_DAYS = 6*20


# ---パラメータメモ---
# ---detect
# coefの何日分かの特徴量の数(特徴選択)
# coefの正負のパターン。coefの0境界以外のパターン。
# 初めてフラグ1が立った時だけ購入、3日連続フラグ、などでシミュレーションのパターン。

# ---sale
# 利益確定は1.1倍か
rikaku_ratio = 1.1
# 損切は0.95倍か
songiri_ratio = 0.95
# 
# 
# 
