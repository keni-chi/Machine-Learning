# jupyter

## 概要
覚書である。順次記載予定。  

## JupyterLab+hubマルチユーザ構築
コンテナ実行
    docker run -d -it --name jupylab -p 8080:8888 -v ~/myJupyterLab:/home/jovyan/workspace -w /workspace continuumio/anaconda3
    docker exec -it jupylab /bin/bash

コンテナ内の準備
    conda install jupyterhub
    cd /opt/conda
    jupyterhub --generate-config
    apt-get update
    apt-get install vim

ユーザ設定
    vi jupyterhub_config.py
    c.Spawner.notebook_dir = '~/notebook'
    c.Spawner.default_url = '/lab'
    c.Spawner.admin_users = {'admin001'}
    c.Spawner.whitelist = {'testuser001', 'testuser002'}

    adduser admin001
        パスワード設定
        Full Name []: 
        Room Number []: 
        Work Phone []: 
        Home Phone []: 
        Other []: 
    adduser testuser001
    adduser testuser002

トークンでの利用
    cd /workspace
    jupyter-lab --notebook-dir=/workspace --ip='*' --port=8888 --no-browser --allow-root
    http://127.0.0.1:8080
    tokenを入力して利用可能

ユーザでの利用
    cd /opt/conda
    jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --port=8888
    http://127.0.0.1:8080
    備考：/home配下にユーザ毎にディレクトリあり。


## 実行結果のスクロールバー
[セル]> [すべての出力]> [スクロールの切り替え](メニューバー上)に移動すると、出力はスクロールなしに戻る



## 参考
[解析環境をJupyterLab+hub-extensionでマルチユーザー化した](https://jun-systems.info/articles/jupyterlab-multi-user/)  

