## tpotインストールのためのxgboostインストール

git clone --recursive http://github.com/dmlc/xgboost

容量オーバーのため以下を実行し、再度cloneしようとしたが失敗
git config --global postBuffer 200M

容量オーバーのため以下を実行し、再度cloneすると成功
git config --global http.postBuffer 2M

>cd xgboost
>mkdir build
>cd build
>cmake .. -G"Visual Studio 15 2017 Win64"

「cmakeをインストール」
https://cmake.org/download/　にてzipをダウンロード
環境変数のパス追加して、cmakeを再実行　例：C:\Program Files\CMake\bin

「Build Tools for Visual Studio 2017のダウンロード」
https://qiita.com/piacerex/items/4d6d234dc0fb66bbb592


2019の場合、cmakeのコマンドは以下でやるとOK（参考：https://xgboost.readthedocs.io/en/latest/build.html#installing-the-development-version-with-visual-studio-windows）※管理者でcmdは不要だった
cmake .. -G"Visual Studio 16 2019" -A x64

開発者コマンドプロンプトを起動

buildフォルダへ移動

MSBuild xgboost.sln

pip install xgboost


## 参考
[tpot公式サンプル](http://epistasislab.github.io/tpot/examples/)  
[windowsでxgboostをビルドし python用パッケージをインストールする方法（メモ）](https://qiita.com/dtsu/items/185e499a4e20a2e458cb)  
[TPOTで自動機械学習（回帰）を試した](https://qiita.com/issakuss/items/f05d90cc5893ecce8b1a)  

