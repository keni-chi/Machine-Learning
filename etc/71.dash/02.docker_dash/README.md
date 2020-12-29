docker build -t hello-dash .
docker run -d -p 8050:8050 hello-dash
http://127.0.0.1:8050/

<エラー時は以下で中に入って、python app.pyで実行して確認>
docker run --rm -it -p 8050:8050 hello-dash sh

<run.shで実行する準備>
chmod 755 *.sh


## 参考
[Bリーグデータを使ってDocker環境でDashとStreamlitを使い比べてみた](https://qiita.com/hikarut/items/bbf099da841bff5e769c)  

