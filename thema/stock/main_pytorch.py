import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# データの準備
data = pd.read_csv('data_20230401/stock_1301.csv')  # 株価データの読み込み
prices = data['Close'].values  # 終値の列を取得
prices = prices.reshape(-1, 1).astype(np.float64)
prices = prices.reshape(-1, 1)  # 2次元に変換

# データの正規化
scaler = MinMaxScaler(feature_range=(0, 1))
prices_scaled = scaler.fit_transform(prices).astype(np.float64)

# データの分割
train_size = int(len(prices_scaled) * 0.7)
train_data = torch.tensor(prices_scaled[:train_size], dtype=torch.double)
test_data = torch.tensor(prices_scaled[train_size:], dtype=torch.double)

# データのバッチ化
def create_batches(data, batch_size):
    # x = []
    # y = []
    # for i in range(len(data) - batch_size):
    #     x.append(data[i:i+batch_size])
    #     y.append(data[i+batch_size])
    # return torch.tensor(x), torch.tensor(y)

    # batches = []
    # for i in range(len(data) - batch_size):
    #     batch = (data[i:i+batch_size], data[i+batch_size])
    #     batches.append(batch)
    # return batches

    # x = []
    # y = []
    # for i in range(len(data) - batch_size):
    #     x.append(torch.tensor(data[i:i+batch_size]))
    #     y.append(torch.tensor(data[i+batch_size]))
    # return [x, y]

    batches = []
    for i in range(len(data) - batch_size):
        inputs = torch.tensor(data[i:i+batch_size])
        inputs = inputs.double()
        targets = torch.tensor(data[i+batch_size])
        batch = (inputs, targets)
        batches.append(batch)
    return batches


batch_size = 32
train_batches = create_batches(train_data, batch_size)

# モデルの定義
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTM, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[-1])
        return out

input_size = 1
hidden_size = 128
output_size = 1

model = LSTM(input_size, hidden_size, output_size)

# モデルの訓練
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 100
for epoch in range(num_epochs):
    epoch_loss = 0.0
    for i, (inputs, targets) in enumerate(train_batches):
        optimizer.zero_grad()
        outputs = model(torch.unsqueeze(inputs, 2))
        loss = criterion(outputs.squeeze(), targets)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss}')

# テストデータでの予測
model.eval()
test_inputs = torch.tensor(test_data[:-1].reshape(1, -1, input_size))
predicted_prices = model(test_inputs.unsqueeze(2)).detach().numpy()
predicted_prices = scaler.inverse_transform(predicted_prices)

# 予測結果のプロット
plt.plot(prices[train_size+1:], label='Actual')
plt.plot(predicted_prices[0], label='Predicted')
plt.legend()
plt.show()