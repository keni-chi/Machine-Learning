# pip install prince pandas matplotlib seaborn

import pandas as pd
import prince
import matplotlib.pyplot as plt
import seaborn as sns

# --- サンプルデータ ---
df = pd.DataFrame({
    "temp":     [20, 21, 19, 23, 22],
    "humidity": [30, 35, 33, 40, 38],
    "steps":    [3000, 5000, 7000, 4000, 6500],
    "sleep":    [6, 7, 8, 5, 7]
})

# グループの指定（列名で指定）
groups = {
    "Sensor": ["temp", "humidity"],
    "Behavior": ["steps", "sleep"]
}

# --- MFA モデル作成 ---
mfa = prince.MFA(
    n_components=2,
)

# --- フィット ---
mfa = mfa.fit(df, groups=groups)

# --- 結果の取得 ---
print("固有値:")
print(mfa.eigenvalues_)

print("\n個体座標:")
row_coord = mfa.row_coordinates(df)
print(row_coord)

print("\n変数座標:")
col_coord = mfa.column_coordinates_
print(col_coord)

# ============================================================
# ① 可視化（散布図：個体プロット）
# ============================================================

plt.figure(figsize=(6, 5))
sns.scatterplot(x=row_coord[0], y=row_coord[1])
for i, txt in enumerate(df.index):
    plt.text(row_coord.iloc[i, 0], row_coord.iloc[i, 1], str(txt))
plt.title("MFA Individual Factor Map")
plt.xlabel("Dim 1")
plt.ylabel("Dim 2")
plt.grid(True)
plt.savefig("mfa_sample_個体プロット.png", dpi=300)
plt.close()

# ============================================================
# ② 可視化（バイプロット：個体 + 変数）
# ============================================================

plt.figure(figsize=(7, 6))
plt.scatter(row_coord[0], row_coord[1], label="Individuals")

# 変数ベクトル
for i in range(col_coord.shape[0]):
    plt.arrow(0, 0, col_coord.iloc[i, 0], col_coord.iloc[i, 1],
              color='red', alpha=0.7)
    plt.text(col_coord.iloc[i, 0], col_coord.iloc[i, 1],
             col_coord.index[i], color='red')

plt.title("MFA Biplot")
plt.xlabel("Dim 1")
plt.ylabel("Dim 2")
plt.grid(True)
# plt.show()
plt.savefig("mfa_sample_個体+変数.png", dpi=300)
plt.close()

# ============================================================
# ③ グループ寄与の計算
# ============================================================

print("\n--- グループ寄与（各次元への寄与） ---")
group_contrib = mfa.row_contributions_
print(group_contrib)

# ============================================================
# ④ カテゴリ変数を含む MFA の例
# ============================================================

df_cat = pd.DataFrame({
    "temp":     [20, 21, 19, 23, 22],
    "humidity": [30, 35, 33, 40, 38],
    "steps":    [3000, 5000, 7000, 4000, 6500],
    "sleep":    [6, 7, 8, 5, 7],
    "gender":   ["M", "F", "F", "M", "F"],   # カテゴリ変数
})

# カテゴリ変数をダミー化
df_cat_dummies = pd.get_dummies(df_cat, columns=["gender"])

groups_cat = {
    "Sensor": ["temp", "humidity"],
    "Behavior": ["steps", "sleep"],
    "Gender": [col for col in df_cat_dummies.columns if "gender" in col]
}

mfa_cat = prince.MFA(n_components=2)
mfa_cat = mfa_cat.fit(df_cat_dummies, groups=groups_cat)

print("\n--- カテゴリ変数を含むMFA：変数座標 ---")
print(mfa_cat.column_coordinates_)

# ============================================================
# ⑤ 実データでの応用例（Iris データ）
# ============================================================

from sklearn.datasets import load_iris
iris = load_iris()
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris["species"] = iris.target

# カテゴリ変数 species をダミー化
df_iris_dummies = pd.get_dummies(df_iris, columns=["species"])

groups_iris = {
    "Morphology": iris.feature_names,
    "Species": [col for col in df_iris_dummies.columns if "species" in col]
}
print('groups_iris')
print(groups_iris)
print('df_iris_dummies')
print(df_iris_dummies)

mfa_iris = prince.MFA(n_components=2)
mfa_iris = mfa_iris.fit(df_iris_dummies, groups=groups_iris)

print("\n--- Iris データのMFA：固有値 ---")
print(mfa_iris.eigenvalues_)

print("\n--- Iris データのMFA：変数座標 ---")
print(mfa_iris.column_coordinates_)
