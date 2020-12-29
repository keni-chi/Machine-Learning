# -*- coding: utf-8 -*-
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sklearn.datasets as datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def analyze():
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
    print(type(X_train))
    print(type(y_train_pred))
    x = X_train[:, 0]
    x = list(range(len(y_train_pred)))
    y = y_train_pred.tolist()
    print('B001')
    print(type(x))
    print(x)
    print(y)
    return x, y



# Dashアプリケーションを作成
app = dash.Dash()

# ヘッダー、ボックス、グラフを含むページを作成
app.layout = html.Div([
    html.H1('==アプリケーションタイトル=='),
    html.Div([html.P('input1')]),
    dcc.Input(id ='input1' 
        ,value=1 # 初期値を設定
    ),
    html.Div([html.P('input2')]),
    dcc.Input(id ='input2' 
        ,value=2 # 初期値を設定
    ),
    dcc.Graph(id='graph1',
        figure={
            'data': []
        }
    )
])


# コールバック関数の追加
@app.callback(
    Output('graph1', 'figure'),
    [Input('input1', 'value'),
     Input('input2', 'value')])

def update_graph(input1, input2):
    # i = random.randint(1, 5)
    print('A001')
    print(input1)
    x , y = analyze()
    print('A002')
    print(input2)
    fig = {
        'data': [
            {'x': x, 'y': y}
        ],
        'layout': {'title':'title_name'}
    }



    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

