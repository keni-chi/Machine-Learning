import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_boston
import pandas as pd


input_size  = 13     # 説明変数の数
output_size = 1     # 推論値の数
alpha       = 0.01  # 学習率
epochs      = 3000  # 学習回数

# network definition
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # self.linear = nn.Linear(input_size, output_size)  # 単層
        self.fc1 = nn.Linear(input_size, 10)  # 説明変数の数
        self.fc2 = nn.Linear(10, 8)
        self.fc3 = nn.Linear(8, output_size)  # 推論値の数

    def forward(self, x): 
        # out = self.linear(x)  # 単層
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)

        return x 

# 確認
boston = load_boston()
df = pd.DataFrame(boston.data, columns=boston.feature_names)
print(df.head())

# 準備
boston = load_boston()
X_train = boston.data
y_train = boston.target
y_train = y_train.reshape(-1, 1)

# 標準化
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)

# PyTorchで取り扱える形式に変換
inputs = torch.from_numpy(X_train_scaled).float()
targets = torch.from_numpy(y_train).float()

# 学習
net = Net()

# 損失関数
loss = nn.MSELoss()

# 最適化関数
optimizer = torch.optim.SGD(net.parameters(), lr=alpha)

# エポックのループを回し、パラメータを更新
for epoch in range(epochs):
    # 勾配のリセット
    optimizer.zero_grad()

    # コストを算出
    outputs = net(inputs)
    cost = loss(outputs, targets)

    # 勾配の計算
    cost.backward()
    optimizer.step()

    # xx回ごとに誤差表示
    if (epoch + 1) % 500 == 0:
        print('Epoch [{}], Loss: {:.4f}'.format(epoch + 1, cost.item()))

# test
inputs = torch.Tensor(X_train_scaled)
results = net(inputs)

for i in range(results.size()[0]):
    if (i) % 50 == 0:
        print('広さ:{}㎡, 築年数:{}, 家賃正解:{:.2f}, 家賃予測:{:.2f}'.format(X_train[i,0], X_train[i,1], y_train[i, 0], results.data[i,0].item()))
