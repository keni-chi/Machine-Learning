import sklearn.datasets as datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from flask import Flask
app = Flask(__name__)


@app.route('/test')
def test(): 
    print('test---start')   


    iris = datasets.load_iris()
    X = iris['data']
    y = iris.target


    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    model = RandomForestClassifier(n_estimators=20,n_jobs=-1)
    model.fit(X_train, y_train)

    print ("train正解率",model.score(X_train, y_train))
    print ("test正解率",model.score(X_test, y_test))

    #予測データ作成
    y_train_pred = model.predict(X_train)


    return {'result': 'test'}


if __name__ == '__main__':
    app.run()
