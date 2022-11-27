import pandas as pd
from sklearn.datasets import load_boston

# データ読み込み
boston = load_boston()
df_X = pd.DataFrame(data=boston.data, columns=boston.feature_names, dtype='float')
df_y = pd.DataFrame(data=boston.target, columns=['MEDV'], dtype='float')
df = pd.concat([df_X, df_y], axis=1)

# Bool列追加
df['MEDV_flg1'] = df['MEDV'] > 22.0
df['MEDV_flg2'] = df['MEDV'] > 30.0

# Bool列でand演算
df['MEDV_flg3'] = df['MEDV_flg1'] * df['MEDV_flg2']

# 「df['CRIM'] >= 0.03」という条件を満たせばMEDVの値、満たさなかったらINDUSの値、をMEDV_num列として追加
df['MEDV_num'] = df['MEDV'].where(df['CRIM'] >= 0.03, df['INDUS'])
print(df)
