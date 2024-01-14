# https://qiita.com/seiji1997/items/bee6b75b4b461ee3a7b2#%E4%BB%8A%E5%9B%9E%E3%81%AE%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%9Flstm%E3%83%A2%E3%83%87%E3%83%AB%E3%81%AE%E7%89%B9%E5%BE%B4
# モジュールのインポート
import numpy as np
import pandas as pd
import pandas_datareader.data as data
from matplotlib import pyplot as plt

# 標準化関数（StandardScaler）をインポート
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import torch
from torch.utils.data import TensorDataset, DataLoader
from torch import nn
import torch.nn.functional as F
from torch import optim


def fit_predict():
    # データの準備
    df = pd.read_csv('data_20230401/stock_1301.csv')  # 株価データの読み込み
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[['Date', 'Close']]
    df.sort_values(by='Date', ascending=True, inplace=True)
    df['25MA'] = df['Close'].rolling(window=25, min_periods=0).mean()
    print(df.head())
    print(df.tail())


    # 可視化
    plt.figure()
    plt.title('Z_Holdings')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.plot(df['Date'], df['Close'], color='black',
            linestyle='-', label='close')
    plt.plot(df['Date'], df['25MA'], color='red',
            linestyle='--', label='25MA')
    plt.legend()  # 凡例
    plt.savefig('./pytorch2/Z_Holdings.png')  # 図の保存
    plt.close()


    # 標準化
    ma = df['25MA'].values.reshape(-1, 1)
    scaler = StandardScaler()
    ma_std = scaler.fit_transform(ma)
    print("ma: {}".format(ma))
    print("ma_std: {}".format(ma_std))


    # 学習・検証データセット作成
    data = []  # 入力データ(過去25日分の移動平均)
    label = []  # 出力データ(1日後の移動平均)
    data_f = []
    label_f = 10*[0]
    for i in range(len(ma_std) - 25):
        if i < (len(ma_std) - 25 - 10):
            data.append(ma_std[i:i + 25])
            label.append(ma_std[i + 25 + 10])  # +9することで2週間後を予測
        else:
            data_f.append(ma_std[i:i + 25])

    print(len(data_f))
    # ndarrayに変換
    data = np.array(data)
    label = np.array(label)
    print("data size: {}".format(data.shape))
    print("label size: {}".format(label.shape))



    # 株価データを訓練データとテストデータに分割
    test_len = int(252)  # 1年分(252日分)
    train_len = int(data.shape[0] - test_len)

    # 訓練データ
    train_data = data[:train_len]
    train_label = label[:train_len]

    # テストデータ
    test_data = data[train_len:]
    test_label = label[train_len:]

    # データの形状を確認
    print("train_data size: {}".format(train_data.shape))
    print("test_data size: {}".format(test_data.shape))
    print("train_label size: {}".format(train_label.shape))
    print("test_label size: {}".format(test_label.shape))


    # ndarrayをPyTorchのTensorに変換
    train_x = torch.Tensor(train_data)
    test_x = torch.Tensor(test_data)
    train_y = torch.Tensor(train_label)
    test_y = torch.Tensor(test_label)


    # 最後にTensorDatasetで特徴量とラベルを結合したデータセットを作成
    train_dataset = TensorDataset(train_x, train_y)
    test_dataset = TensorDataset(test_x, test_y)


    # DataLoaderを使用して、データセットを128個のミニバッチに分割します。
    train_batch = DataLoader(
        dataset=train_dataset,  # データセットの指定
        batch_size=128,  # バッチサイズの指定
        shuffle=True,  # シャッフルするかどうかの指定
        num_workers=0)  # コアの数
    test_batch = DataLoader(
        dataset=test_dataset,
        batch_size=128,
        shuffle=False,
        num_workers=0)

    # ミニバッチデータセットの確認
    for data, label in train_batch:
        print("batch data size: {}".format(data.size()))  # バッチの入力データサイズ
        print("batch label size: {}".format(label.size()))  # バッチのラベルサイズ
        break


    # モデル構造
    # 1層のLSTMと、１層の全結合層で構成しています。
    class Net(nn.Module):
        def __init__(self, D_in, H, D_out):
            super(Net, self).__init__()
            self.lstm = nn.LSTM(D_in, H, batch_first=True,
                                num_layers=1)
            self.linear = nn.Linear(H, D_out)

        def forward(self, x):
            output, (hidden, cell) = self.lstm(x)
            output = self.linear(output[:, -1, :])
            return output


    #ハイパーパラメータの定義
    D_in = 1  # 入力次元: 1
    H = 200  # 隠れ層次元: 200
    D_out = 1  # 出力次元: 1
    epoch = 3  # 学習回数: 100


    # CPUとGPUどちらを使うかを指定します。
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = Net(D_in, H, D_out).to(device)
    print("Device: {}".format(device))


    # 損失関数(平均二乗誤差: MSE)の定義と最適化関数(Adam)の定義
    criterion = nn.MSELoss() 
    optimizer = optim.Adam(net.parameters())


    # 学習・評価損失を保存するリストを作成。学習を実行
    train_loss_list = []  # 学習損失
    test_loss_list = []  # 評価損失

    # 学習（エポック）の実行
    for i in range(epoch):
        # エポックの進行状況を表示
        print('---------------------------------------------')
        print("Epoch: {}/{}".format(i+1, epoch))

        # 損失の初期化
        train_loss = 0  # 学習損失
        test_loss = 0  # 評価損失

        # ---------学習パート--------- #
        # ニューラルネットワークを学習モードに設定
        net.train()
        # ミニバッチごとにデータをロードし学習
        for data, label in train_batch:
            # GPUにTensorを転送
            data = data.to(device)
            label = label.to(device)

            # 勾配を初期化
            optimizer.zero_grad()
            # データを入力して予測値を計算（順伝播）
            y_pred = net(data)
            # 損失（誤差）を計算
            loss = criterion(y_pred, label)
            # 勾配の計算（逆伝搬）
            loss.backward()
            # パラメータ（重み）の更新
            optimizer.step()
            # ミニバッチごとの損失を蓄積
            train_loss += loss.item()

        # ミニバッチの平均の損失を計算
        batch_train_loss = train_loss / len(train_batch)
        # ---------学習パートはここまで--------- #

        # ---------評価パート--------- #
        # ニューラルネットワークを評価モードに設定
        net.eval()
        # 評価時の計算で自動微分機能をオフにする
        with torch.no_grad():
            for data, label in test_batch:
                # GPUにTensorを転送
                data = data.to(device)
                label = label.to(device)
                # データを入力して予測値を計算（順伝播）
                y_pred = net(data)
                # 損失（誤差）を計算
                loss = criterion(y_pred, label)
                # ミニバッチごとの損失を蓄積
                test_loss += loss.item()

        # ミニバッチの平均の損失を計算
        batch_test_loss = test_loss / len(test_batch)
        # ---------評価パートはここまで--------- #

        # エポックごとに損失を表示
        print("Train_Loss: {:.2E} Test_Loss: {:.2E}".format(
            batch_train_loss, batch_test_loss))
        # 損失をリスト化して保存
        train_loss_list.append(batch_train_loss)
        test_loss_list.append(batch_test_loss)


    # 損失
    plt.figure()
    plt.title('Train and Test Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(range(1, epoch+1), train_loss_list, color='blue',
            linestyle='-', label='Train_Loss')
    plt.plot(range(1, epoch+1), test_loss_list, color='red',
            linestyle='--', label='Test_Loss')
    plt.legend()  # 凡例
    plt.savefig('./pytorch2/損失.png')  # 図の保存
    plt.close()


    # 予測
    net.eval()
    # 推定時の計算で自動微分機能をオフにする
    with torch.no_grad():
        # 初期化
        pred_ma = []
        true_ma = []
        for data, label in test_batch:
            # GPUにTensorを転送
            data = data.to(device)
            label = label.to(device)
            # 予測値を計算：順伝播
            y_pred = net(data)
            pred_ma.append(y_pred.view(-1).tolist())
            true_ma.append(label.view(-1).tolist())


    # 標準化を解除して元の株価に変換
    pred_ma = np.array([elem for lst in pred_ma for elem in lst]).reshape(-1, 1)
    true_ma = np.array([elem for lst in true_ma for elem in lst]).reshape(-1, 1)
    pred_ma = scaler.inverse_transform(pred_ma)
    true_ma = scaler.inverse_transform(true_ma)


    # 平均絶対誤差を計算
    mae = mean_absolute_error(true_ma, pred_ma)
    print("MAE: {:.3f}".format(mae))


    # 最後に終値と25日移動平均を図示
    date = df['Date'][-1*test_len:]  # テストデータの日付
    test_close = df['Close'][-1*test_len:].values.reshape(-1)  # テストデータの終値
    plt.figure()
    plt.title('YHOO Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.plot(date, test_close, color='black',
            linestyle='-', label='close')
    plt.plot(date, true_ma, color='dodgerblue',
            linestyle='--', label='true_25MA')
    plt.plot(date, pred_ma, color='red',
            linestyle=':', label='predicted_25MA')
    plt.legend()  # 凡例
    plt.xticks(rotation=30)  
    plt.savefig('./pytorch2/予測結果.png')  # 図の保存
    plt.close()


def main():
    fit_predict()


if __name__ == '__main__':
    main()
