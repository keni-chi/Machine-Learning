import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

input_size  = 4     # 説明変数の数
output_size = 3     # 推論値の数
alpha       = 0.01  # 学習率
epochs      = 3000  # 学習回数

# network definition
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, 10)  # 説明変数の数4
        self.fc2 = nn.Linear(10, 8)
        self.fc3 = nn.Linear(8, output_size)  # 推論値の数3

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 準備
iris = datasets.load_iris()
y = np.zeros((len(iris.target), 1 + iris.target.max()), dtype=int)  # one hot encode枠
y[np.arange(len(iris.target)), iris.target] = 1  # one hot encode
X_train, X_test, y_train, y_test = train_test_split(iris.data, y, test_size=0.25)

# PyTorchで取り扱える形式に変換
inputs = Variable(torch.from_numpy(X_train).float(), requires_grad=True)
targets = Variable(torch.from_numpy(y_train).float())

# 学習
net = Net()

# 最適化関数
optimizer = optim.SGD(net.parameters(), lr=alpha)  # 学習率

# 損失関数
mse_loss = nn.MSELoss()

# エポックのループを回し、パラメータを更新
for epoch in range(epochs):  # 学習回数
    # 勾配のリセット
    optimizer.zero_grad()  

    # コストを算出
    output = net(inputs)
    loss = mse_loss(output, targets)

    # 勾配の計算
    loss.backward()
    optimizer.step()

    # xx回ごとに誤差表示
    if (epoch + 1) % 500 == 0:
        print('Epoch [{}], Loss: {:.4f}'.format(epoch + 1, loss.item()))


# test
outputs = net(Variable(torch.from_numpy(X_test).float()))
_, predicted = torch.max(outputs.data, 1)
y_predicted = predicted.numpy()
y_true = np.argmax(y_test, axis=1)

# 集計
accuracy = (int)(100 * np.sum(y_predicted == y_true) / len(y_predicted))
print('accuracy: {0}%'.format(accuracy))


# utility function to predict for an unknown data
def predict(X):
    X = Variable(torch.from_numpy(np.array(X)).float())
    outputs = net(X)
    return np.argmax(outputs.data.numpy())
