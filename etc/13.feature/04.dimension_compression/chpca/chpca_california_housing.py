import numpy as np
from scipy.signal import hilbert
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -----------------------------
# 複素ヒルベルト PCA 関数
# -----------------------------
def complex_hilbert_pca(X, n_components=4):
    """
    複素ヒルベルト主成分分析 (Complex Hilbert PCA)
    """
    # Step 1: Hilbert transform → complex analytic signal
    Xc = hilbert(X, axis=0)

    # Step 2: Complex covariance matrix
    C = np.dot(Xc.conj().T, Xc) / Xc.shape[0]

    # Step 3: Eigen decomposition
    eigvals, eigvecs = np.linalg.eigh(C)

    # Sort by eigenvalue (descending)
    idx = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, idx]

    # Step 4: Project onto principal components
    Z = np.dot(Xc, eigvecs[:, :n_components])

    return Z, eigvecs[:, :n_components]


# -----------------------------
# California Housing データ読み込み
# -----------------------------
data = fetch_california_housing()
X = data.data
y = data.target
feature_names = data.feature_names

# -----------------------------
# X と y のヘッダ情報を表示
# -----------------------------
print("=== X の特徴量名（ヘッダ） ===")
print(feature_names)

print("\n=== y の説明（ターゲット名） ===")
print("Median House Value (in $100,000s)")

print("\nX shape:", X.shape)
print("y shape:", y.shape)


# -----------------------------
# CHPCA による次元削減（主成分 4）
# -----------------------------
Z, components = complex_hilbert_pca(X, n_components=4)  # Z: 複素主成分スコア（サンプル数 × 4）,   components: 主成分ベクトル（特徴量数 × 4）
print(Z.shape)
print(Z)
print(components.shape)
print(components)

# 実部と虚部を特徴量として使う
Z_real_imag = np.hstack([Z.real, Z.imag])
print(Z_real_imag.shape)
print(Z_real_imag)

# -----------------------------
# 学習・評価
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    Z_real_imag, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("MSE:", mse)
print("回帰係数（実部＋虚部）:")
print(model.coef_)
