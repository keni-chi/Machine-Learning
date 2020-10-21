# -*- coding: utf-8 -*-
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sklearn.datasets as datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# Dashアプリケーションを作成
app = dash.Dash()

# ヘッダー、ボックス、グラフを含むページを作成
app.layout = html.Div([
    html.H1('H1_tag'),
    html.H3('H3_tag'),
    html.Div([html.P('x1')]),
    dcc.Input(id ='x1' 
        ,value='1' # 初期値を設定
    ),
    html.Div([html.P('x2')]),
    dcc.Input(id ='x2' 
        ,value='2' # 初期値を設定
    ),
    dcc.Graph(id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])


# コールバック関数の追加
@app.callback(
    Output('my_graph', 'figure'),
    [Input('x1', 'value'),
     Input('x2', 'value')])
def update_graph(x1_value, x2_value):
    i = random.randint(1, 5)
    fig = {
        'data': [
            {'x': [1,2], 'y': [x1_value, x2_value]}
        ],
        'layout': {'title':'title_name'}
    }


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
    print(y_train_pred)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

