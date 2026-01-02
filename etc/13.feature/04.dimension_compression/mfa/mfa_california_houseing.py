# pip install prince pandas matplotlib seaborn scikit-learn

import pandas as pd
import prince
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing

# ============================================================
# 0. California Housing データの読み込み
# ============================================================

cal = fetch_california_housing(as_frame=True)
df = cal.frame  # 8つの説明変数 + 目的変数 MedHouseVal

# 元の列名の確認（参考）
# print(df.columns)
# Index(['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms',
#        'Population', 'AveOccup', 'Latitude', 'Longitude', 'MedHouseVal'])

# ============================================================
# 1. MFA のためのグループ設定
# ============================================================

# ここでは例として、以下のようにグルーピングする：
# - Income_House: 世帯収入・家の年数・世帯人数
# - House_Structure: 部屋数関連
# - Area: 地域・位置情報
groups = {
    "Income_House": ["MedInc", "HouseAge", "AveOccup"],
    "House_Structure": ["AveRooms", "AveBedrms"],
    "Area": ["Population", "Latitude", "Longitude"],
}

# 今回は説明変数のみを使って MFA（目的変数 MedHouseVal は除く）
df_mfa = df[list(set(sum(groups.values(), [])))]  # groups で使う列だけ抽出

# サンプルサイズが大きいので、例として 2000 行だけ使う
df_mfa = df_mfa.sample(n=2000, random_state=0).reset_index(drop=True)

# ============================================================
# 2. MFA モデル作成 & フィット
# ============================================================

mfa = prince.MFA(
    n_components=2,
)

mfa = mfa.fit(df_mfa, groups=groups)

# ============================================================
# 3. 結果の取得（固有値・個体座標・変数座標）
# ============================================================

print("固有値:")
print(mfa.eigenvalues_)

print("\n個体座標:")
row_coord = mfa.row_coordinates(df_mfa)
print(row_coord.head())

print("\n変数座標:")
col_coord = mfa.column_coordinates_
print(col_coord)

# ============================================================
# ① 可視化（散布図：個体プロット）
# ============================================================

plt.figure(figsize=(6, 5))
sns.scatterplot(x=row_coord[0], y=row_coord[1], s=15, alpha=0.6)
# 多いのでラベルは付けない（必要なら一部だけ付けてもよい）
plt.title("MFA Individual Factor Map (California Housing)")
plt.xlabel("Dim 1")
plt.ylabel("Dim 2")
plt.grid(True)
plt.savefig("california_mfa_個体プロット.png", dpi=300)
plt.close()

# ============================================================
# ② 可視化（バイプロット：個体 + 変数）
# ============================================================

plt.figure(figsize=(7, 6))
plt.scatter(row_coord[0], row_coord[1], label="Individuals", s=10, alpha=0.4)

# 変数ベクトル
for i in range(col_coord.shape[0]):
    plt.arrow(0, 0, col_coord.iloc[i, 0], col_coord.iloc[i, 1],
              color='red', alpha=0.7, head_width=0.02)
    plt.text(col_coord.iloc[i, 0], col_coord.iloc[i, 1],
             col_coord.index[i], color='red')

plt.title("MFA Biplot (California Housing)")
plt.xlabel("Dim 1")
plt.ylabel("Dim 2")
plt.grid(True)
plt.savefig("california_mfa_個体+変数.png", dpi=300)
plt.close()

# ============================================================
# ③ 寄与の確認（ここでは行寄与）
# ============================================================

print("\n--- 行寄与（各サンプルが次元に与える寄与） ---")
row_contrib = mfa.row_contributions_
print(row_contrib.head())

# ============================================================
# ④ カテゴリ変数を含む MFA の例
#     → California Housing から地域カテゴリを作る
# ============================================================

# 例: 緯度で「北」「南」のカテゴリを作る
lat_median = df["Latitude"].median()
df_cat = df_mfa.copy()
df_cat["Region_NS"] = (df["Latitude"].loc[df_mfa.index] > lat_median).map({True: "North", False: "South"})

# カテゴリ変数をダミー化
df_cat_dummies = pd.get_dummies(df_cat, columns=["Region_NS"])

groups_cat = {
    "Income_House": ["MedInc", "HouseAge", "AveOccup"],
    "House_Structure": ["AveRooms", "AveBedrms"],
    "Area": ["Population", "Latitude", "Longitude"],
    "Region": [col for col in df_cat_dummies.columns if "Region_NS" in col],
}

mfa_cat = prince.MFA(n_components=2)
mfa_cat = mfa_cat.fit(df_cat_dummies, groups=groups_cat)

print("\n--- カテゴリ変数（Region_NS）を含むMFA：変数座標 ---")
print(mfa_cat.column_coordinates_)

# ============================================================
# ⑤ 実データでの応用例（別のグルーピングで再度 MFA）
# ============================================================

# 例: 目的変数 MedHouseVal を含めたグルーピングを試す
#    - Socio: MedInc, HouseAge, Population, AveOccup
#    - Structure: AveRooms, AveBedrms
#    - Location: Latitude, Longitude
#    - Target: MedHouseVal（ダミーではなくそのまま）

df_2 = df.sample(n=2000, random_state=1).reset_index(drop=True)

groups_housing = {
    "Socio": ["MedInc", "HouseAge", "Population", "AveOccup"],
    "Structure": ["AveRooms", "AveBedrms"],
    "Location": ["Latitude", "Longitude"],
    "Target": ["MedHouseVal"],
}

mfa_housing = prince.MFA(n_components=2)
mfa_housing = mfa_housing.fit(df_2, groups=groups_housing)

print("\n--- California Housing (別グループ構成) のMFA：固有値 ---")
print(mfa_housing.eigenvalues_)

print("\n--- California Housing (別グループ構成) のMFA：変数座標 ---")
print(mfa_housing.column_coordinates_)
