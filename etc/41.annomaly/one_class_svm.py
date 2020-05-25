import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

def main():
    print('------------01')
    iris = load_iris()
    pca = PCA(n_components=2)
    data = pca.fit_transform(iris.data)
    print(type(data))
    print(data)
    # nuで異常値の割合を指定。predictすると正常値=1,異常値=-1。
    ocsvm = OneClassSVM(nu=0.1, gamma="auto")
    ocsvm.fit(data)
    preds = ocsvm.predict(data)
    print(preds)
    plt.scatter(data[:,0], data[:,1], c=preds, cmap=plt.cm.RdBu)
    plt.show()

    print('------------02A')
    x = np.linspace(-5, 5, 500)
    y = np.linspace(-1.5, 1.5, 250)    
    X, Y = np.meshgrid(x, y)
    print('X.ravel():')
    print(X.ravel())
    print(X.shape)
    print(Y.shape)
    z1 = np.array([X.ravel(), Y.ravel()])
    print(z1.shape)
    z2 = ocsvm.decision_function(
        np.array([X.ravel(), Y.ravel()]).T)
    print(z2.shape)
    # (250, 500)
    # (250, 500)
    # (2, 125000)
    # (125000,)
    # (250, 500)
    print(z2.reshape(X.shape).shape)
    df = ocsvm.decision_function(
        np.array([X.ravel(), Y.ravel()]).T).reshape(X.shape)
    plt.scatter(data[:,0], data[:,1], c=preds, cmap=plt.cm.RdBu, alpha=0.8)
    r = max([abs(df.min()), abs(df.max())])
    print('------------02B')
    print(df.min())
    print(max([abs(df.min()), abs(df.max())]))
    print(df)
    plt.contourf(X, Y, df, 10, vmin=-r, vmax=r, cmap=plt.cm.RdBu, alpha=.5)
    plt.show()


if __name__ == "__main__":
    main()
