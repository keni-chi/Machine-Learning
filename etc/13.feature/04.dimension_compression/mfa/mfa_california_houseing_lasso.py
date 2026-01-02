# pip install prince pandas scikit-learn matplotlib seaborn

import pandas as pd
import prince
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ============================================================
# 1. California Housing データの読み込み
# ============================================================

cal = fetch_california_housing(as_frame=True)
df = cal.frame

# 目的変数
y = df["MedHouseVal"]

# 説明変数（MFA に使う列）
X = df.drop(columns=["MedHouseVal"])

# ============================================================
# 2. グループ設定（例）
# ============================================================

groups = {
    "Income_House": ["MedInc", "HouseAge", "AveOccup"],
    "House_Structure": ["AveRooms", "AveBedrms"],
    "Area": ["Population", "Latitude", "Longitude"],
}

# ============================================================
# 3. MFA による次元圧縮（3次元）
# ============================================================
N = 5
mfa = prince.MFA(
    n_components=N,   # ★ 3次元に圧縮
)

mfa = mfa.fit(X, groups=groups)

# 圧縮後の特徴量（N次元）
X_mfa = mfa.row_coordinates(X)
# X_mfa.columns = ["MFA1", "MFA2", "MFA3"]
X_mfa.columns = ["MFA1", "MFA2", "MFA3", "MFA4", "MFA5"]

print("\n--- MFA N次元特徴量（先頭5行） ---")
print(X_mfa.head())

# ============================================================
# 4. 学習データ / テストデータ分割（7:3）
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X_mfa, y, test_size=0.3, random_state=42
)

# ============================================================
# 5. Lasso 回帰による価格予測
# ============================================================

lasso = Lasso(alpha=0.001, random_state=42)
lasso.fit(X_train, y_train)

# 予測
y_pred = lasso.predict(X_test)

# ============================================================
# 6. 精度評価
# ============================================================

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n==============================")
print(" Lasso × MFA(3次元) 結果")
print("==============================")
print(f"RMSE: {rmse:.4f}")
print(f"R²:   {r2:.4f}")

# ============================================================
# 7. 予実散布図（実測値 vs 予測値）
# ============================================================

plt.figure(figsize=(6, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         color="red", linestyle="--", label="y = x")

plt.xlabel("Actual Price (MedHouseVal)")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted (Lasso + MFA)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("california_mfa_lasso_予実散布図.png", dpi=300)
plt.close()
