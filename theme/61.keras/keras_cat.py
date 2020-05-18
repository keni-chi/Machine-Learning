import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from sklearn.metrics import confusion_matrix

def plot_history(history):
	# Setting Parameters
	acc = history.history['accuracy']
	loss = history.history['loss']
	epochs = range(len(acc))

	# Accracy
	plt.plot(epochs, acc, 'bo' ,label = 'training acc')
	plt.title('acc')
	plt.legend()
	plt.figure()

	# Loss
	plt.plot(epochs, loss, 'bo' ,label = 'training loss')
	plt.title('loss')
	plt.legend()
	plt.show()

# iris データセットをロード
iris = datasets.load_iris()
X = iris['data']
y = iris['target']

# 変換
X_scale = preprocessing.scale(X)
y_cat = np_utils.to_categorical(y)

# 学習データとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X_scale, y_cat, random_state=0)

# model ################################
model = Sequential() 

# Denseの第一引数は隠れ層のニューロン数を、第二引数は入力層をタプル形式で指定

# Flatten層
# Flatten層では、画像などで2次元配列を平坦化して1次元配列的に直す。
# model.add(Flatten(input_shape=(28, 28)))

# Dense層
# 前層と当該層のあいだを全結合（密結合）した全結合層。

# 入力層
# model.add(Dense(16, input_dim=4))  # こちらの書き方でもOK
model.add(Dense(32, input_shape=(4,)))
model.add(Activation('relu'))

# 中間層
model.add(Dense(16, activation='relu'))  # 1行にまとめられる
model.add(Dropout(0.2))  # 前層から次層への出力を遮断する。0.0に設定すると、実質的にDropout層が存在しないのと同じ。
model.add(Dense(8, activation='sigmoid'))  # 1行にまとめられる

 # 出力層
model.add(Dense(3))
model.add(Activation('softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# fit
history = model.fit(X_train, y_train, epochs=20, batch_size=1, verbose=1)

# evaluate #################################
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print('Accuracy', '{:.2f}'.format(accuracy))

# モデルの概要を表示
model.summary()

# # historyをプロット
# plot_history(history)

# predict ################################
y_pred = model.predict_classes(X_test)

# oheを元に戻す
y_test_decode = np.argmax(y_test, axis=1)

# 予測と正解の比較
fig = plt.figure(figsize=(14,7))
ax = fig.add_subplot(111)
ax.scatter(2,2,color="white")
ax.plot(y_pred,lw=1,color="red",label="y_pred")
ax.plot(y_test_decode,lw=1,color="blue",label="y_test_decode")
ax.legend()
plt.show()

# 混同行列
con = confusion_matrix(y_pred, y_test_decode)
print(con)
