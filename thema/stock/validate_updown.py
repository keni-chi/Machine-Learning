import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


class ValidateUpdate():

    def __init__(self):
        pass

    def run(self):
        for code in ['7203']:
            df = self.read_code_data(code)
            self.validate(df)

    def read_code_data(self, code):
        df = pd.read_csv(f'./data-yahoo-20231203/stock_{code}.csv',index_col=0)

        # 時系列特徴量の追加
        df_close= df[['Close']]
        for i in range(1,6):
            df_temp = df_close.rename(columns={'Close': 'CloseBefore'+str(i)}).shift(i)
            df = pd.concat([df, df_temp], axis=1)

        # 目的変数の追加
        df['target_value'] = df['Close'].shift(-5)
        # 値上がりしていると1,値下がりしていると0
        df.loc[df['Close']*1.1 <= df['target_value'], 'target'] = 'up'
        df.loc[df['Close']*0.9 > df['target_value'], 'target'] = 'down'

        # null削除
        df = df.dropna()

        return df

    def validate(self, df):
        pass
        # trainとtest分割
        train_data = df[df.index < "2018-01-01"]
        test_data = df[df.index >= "2018-01-01"]

        # Xとy分割
        X_train = train_data.drop(['target', 'target_value'], axis=1)
        X_test = test_data.drop(['target', 'target_value'], axis=1)
        y_train = train_data[['target']]
        y_test = test_data[['target']]

        # 学習
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # 予測
        y_pred = model.predict(X_test)

        # 重要特徴量
        # labels = X_train.columns
        # importances = model.feature_importances_
        # plt.figure(figsize = (10,6))
        # plt.barh(y = range(len(importances)), width = importances)
        # plt.yticks(ticks = range(len(labels)), labels = labels)
        # plt.show()
        # 重要度順を取得
        sorted_idx = model.feature_importances_.argsort()
        # プロット
        fig, ax = plt.subplots(figsize=(20, 40))
        plt.rcParams["font.size"] = 12
        ax.barh(X_train.columns[sorted_idx], model.feature_importances_[sorted_idx])
        ax.set_xlabel("Random Forest Feature Importance")
        plt.tight_layout()
        plt.show()
        plt.close()

        #モデルを作成する段階でのモデルの識別精度
        trainaccuracy_random_forest = model.score(X_train, y_train)
        print('TrainAccuracy: {}'.format(trainaccuracy_random_forest))

        #作成したモデルに学習に使用していない評価用のデータセットを入力し精度を確認
        accuracy_random_forest = accuracy_score(y_test, y_pred)
        print('Accuracy: {}'.format(accuracy_random_forest))

        #confusion matrix
        mat = confusion_matrix(y_test, y_pred, labels=['up', 'down'])
        print(mat)
        sns.heatmap(mat, square=True, annot=True, cbar=False, fmt='d', cmap='RdPu')
        plt.xlabel('predicted class')
        plt.ylabel('true value')
        plt.show()


if __name__ == '__main__':
    ValidateUpdate().run()
