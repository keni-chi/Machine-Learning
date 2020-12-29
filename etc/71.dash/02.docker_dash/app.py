# -*- coding: utf-8 -*-
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output, State

import sklearn.datasets as datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


def plot_pred_and_actual(y_pred, y_actual):
    fig = plt.figure(figsize=(14,7))
    ax = fig.add_subplot(111)
    ax.scatter(2,2,color="white")
    ax.plot(y_pred,lw=1,color="red",label="y_pred")
    ax.plot(y_actual,lw=1,color="blue",label="y_actual")
    ax.legend()
    # plt.show()
    fig.savefig("image.png")


def analyze(rs):
    print('analyze----------------start')
    iris = datasets.load_iris()
    X = iris['data']
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rs)

    model = RandomForestClassifier(n_estimators=20)
    model.fit(X_train, y_train)

    print ("train正解率",model.score(X_train, y_train))
    print ("test正解率",model.score(X_test, y_test))

    #予測データ作成
    y_train_pred = model.predict(X_train)
    x = X_train[:, 0]
    x = list(range(len(y_train_pred)))
    y = y_train_pred.tolist()

    print('accuracy_score: ')
    acc = accuracy_score(y_train, y_train_pred)
    print(acc)

    plot_pred_and_actual(y_train, y_train_pred)

    return x, y, acc

image_filename = 'image.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


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
    html.Br(),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="30%", width="30%"),
    html.Br(),
    html.Button(id="submit-button", n_clicks=0, children="Submit"),
    dcc.Graph(id='graph1',
        figure={
            'data': []
        }
    )
])


# コールバック関数の追加
@app.callback(
    Output('graph1', 'figure'),
    [Input("submit-button", "n_clicks")],
    [State("input1", "value"),
     State("input2", "value")])

def update_graph(n_clicks, input1, input2):
    print('update_graph----------------start')
    x , y, acc = analyze(int(input1) + int(input2))
    fig = {
        'data': [
            {'x': x, 'y': y}
        ],
        'layout': {'title':'title_name: '+ str(acc)}
    }



    return fig


if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port=8050, debug=True)

