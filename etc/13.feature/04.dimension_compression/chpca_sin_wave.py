import numpy as np
from scipy.signal import hilbert
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

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
# ダミーデータ生成（1000 行・sin 波 10 周期）
# -----------------------------
N = 100
cycles = 10
t = np.linspace(0, cycles * 2 * np.pi, N)  # ★ 10周期のsin波
print(t)

# 目的変数（完全にきれいな sin 波）
y = np.sin(t + np.pi / 8)

# 特徴量 8 列：π/4 ずつ位相をずらす（ノイズは極小）
X = []
for k in range(8):
    phase = k * (np.pi / 4)
    noise = 0.005 * np.random.randn(N)  # ★ ノイズを極小に
    clean_wave = np.sin(t + phase)
    X.append(clean_wave + noise)

X = np.vstack(X).T  # shape = (1000, 8)


# -----------------------------
# CHPCA による次元削減（主成分 4）
# -----------------------------
Z, components = complex_hilbert_pca(X, n_components=4)

# 実部と虚部を特徴量として使う
Z_real_imag = np.hstack([Z.real, Z.imag])

# -----------------------------
# 学習・評価
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    Z_real_imag, y, test_size=0.2, random_state=42, shuffle=False
)

model = LinearRegression()
model.fit(X_train, y_train)

# 予測
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# MSE
mse = mean_squared_error(y_test, y_test_pred)
print("\n=== 回帰結果 ===")
print("MSE:", mse)


# -----------------------------
# 可視化（折れ線グラフ）
# -----------------------------
plt.figure(figsize=(12, 8))

# --- Train ---
plt.subplot(2, 1, 1)
plt.plot(y_train, label="Train True", linewidth=2)
plt.plot(y_train_pred, label="Train Pred", linestyle="--")
plt.title("Train Data: True vs Predicted")
plt.legend()
plt.grid(True)

# # --- Test ---
plt.subplot(2, 1, 2)
plt.plot(y_test, label="Test True", linewidth=2)
plt.plot(y_test_pred, label="Test Pred", linestyle="--")
plt.title("Test Data: True vs Predicted")
plt.legend()
plt.grid(True)

plt.tight_layout()

# 画像保存
plt.savefig("chpca_sin_prediction_1000rows_10cycles.png", dpi=300)

plt.show()
plt.close()

# -----------------------------
# 特徴量 8 個の可視化
# -----------------------------
plt.figure(figsize=(12, 10))

for i in range(8):
    plt.subplot(4, 2, i+1)
    plt.plot(X[:, i], linewidth=1.5)
    plt.title(f"Feature {i+1}: sin(t + {i}π/4) + noise")
    plt.grid(True)

plt.tight_layout()
plt.savefig("features_8waves.png", dpi=300)
plt.show()
plt.close()


# -----------------------------
# 特徴量 8 個を 1 画像に重ね描き（8 色）
# -----------------------------
plt.figure(figsize=(12, 5))

colors = plt.cm.tab10(np.linspace(0, 1, 8))  # 8 色を自動生成

for i in range(8):
    plt.plot(X[:, i], color=colors[i], label=f"Feature {i+1} (phase={i}π/4)", linewidth=1.5)

plt.title("All 8 Features (Phase-shifted Sine Waves)")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend(loc="upper right")
plt.grid(True)

plt.tight_layout()
plt.savefig("features_8waves_overlay.png", dpi=300)
plt.show()
