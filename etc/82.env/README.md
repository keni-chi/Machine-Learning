# etc

## 概要
覚書である。順次記載予定。  


## conda
### create,activate,export,create
conda create -n cenv
conda activate cenv
conda install requests
conda env export > cenv2.yaml
conda deactivate

conda env create -f cenv2.yaml
conda activate cenv2

### jupyterへ追加
ipython kernel install --user --name=cenv2

## venv

参考：https://qiita.com/Gattaca/items/80a5d36673ba2b6ef7f0
### jupyterへ追加
ipython kernel install --user --name=.venv

---batファイル---
cd C:\xxxxxx
jupyter notebook
------------------

## 参考
