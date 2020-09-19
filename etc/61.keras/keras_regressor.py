import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, BatchNormalization
from sklearn.metrics import confusion_matrix


def plot_regressor(pred, actual):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    ax.scatter(pred, actual, marker='o')
    ax.set_title('pred vs actual')
    ax.set_xlabel('pred')
    ax.set_ylabel('actual')
    lims = [0, 100]
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
    plt.grid()
    plt.show()


def plot_history(history):
    # Setting Parameters
    mae = history.history['mae']
    loss = history.history['loss']
    val_mae = history.history['val_mae']
    val_loss = history.history['val_loss']
    epochs = range(len(mae))

    # mae
    plt.figure()
    plt.plot(epochs, mae, marker='o' ,label = 'training mae')
    plt.plot(epochs, val_mae, marker='^' ,label = 'val_mae')
    plt.title('mae')
    plt.legend()
    plt.show()

    # Loss 訓練データの損失
    plt.plot(epochs, loss, marker='o' ,label = 'training loss')
    plt.plot(epochs, val_loss, marker='^' ,label = 'val_loss')
    plt.title('loss')
    plt.legend()
    plt.show()


# データ読み込み
boston = load_boston()
X_array = boston.data
y_array = boston.target
print(X_array.shape)
print(y_array)
X_train, X_test, y_train, y_test = train_test_split(X_array, y_array, test_size=0.2, random_state=0)

#トレーニングデータの正規化
# X_train_mean = X_train.mean(axis=0)
# X_train_std = X_train.std(axis=0)
# X_train -= X_train_mean
# X_train /= X_train_std
 
# y_train_mean = y_train.mean()
# y_train_std = y_train.std()
# y_train -= y_train_mean
# y_train /= y_train_std

#テストデータの正規化
# X_test -= X_train_mean
# X_test /= X_train_std
# y_test -= y_train_mean
# y_test /= y_train_std

# 正規化
sc1 = StandardScaler()
sc1.fit(X_train)
X_train_std = sc1.transform(X_train)
X_test_std = sc1.transform(X_test)

sc2 = StandardScaler()
sc2.fit(y_train.reshape(-1, 1))
y_train_std = sc2.transform(y_train.reshape(-1, 1))
y_test_std = sc2.transform(y_test.reshape(-1, 1))

model = Sequential()
print((X_train_std.shape[1],))
# model.add(Dense(64, activation='relu', input_shape=(X_train_std.shape[1],)))
model.add(Dense(64, input_shape=(X_train_std.shape[1],)))
model.add(Activation('relu'))

# model.add(Dense(32))
# model.add(BatchNormalization())
# model.add(Activation('relu'))
# model.add(Dropout(0.5))

model.add(Dense(1))
model.compile(optimizer='adam', 
              loss='mse', 
              metrics=['mae'])

history = model.fit(X_train, y_train,  #トレーニングデータ
                    batch_size=1,  #バッチサイズの指定
                    epochs=20,      #エポック数の指定
                    verbose=1,       #ログ出力の指定.
                    validation_data=(X_test_std, y_test_std))  #テストデータ

# evaluate #################################
loss, accuracy = model.evaluate(X_test_std, y_test_std, verbose=0)
print('Accuracy', '{:.2f}'.format(accuracy))

# モデルの概要を表示
model.summary()

# historyをプロット
plot_history(history)

# predict ################################
y_train_pred = model.predict(X_train_std)
y_test_pred = model.predict(X_test_std)


y_train_pred_inv = sc2.inverse_transform(y_train_pred).flatten()
y_test_pred_inv = sc2.inverse_transform(y_test_pred).flatten()

plot_regressor(y_train_pred_inv, y_train)
plot_regressor(y_test_pred_inv, y_test)

# print(y_train_std)
# print(y_test_std)

# print(y_train_pred)
# print(y_test_pred)

# print(y_train_pred_inv)
# print(y_test_pred_inv)
