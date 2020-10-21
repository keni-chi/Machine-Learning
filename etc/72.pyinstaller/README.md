# pyinstaller

## 概要
覚書である。順次記載予定。

pip install flask pyinstaller

pyinstaller main.py --onefile

main.specのhiddenimportsのlistに追記 (hiddenimports=['sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils'],)
pyinstaller main.spec


## 参考
[PythonによるWeb APIをEXE化する](https://qiita.com/shindooo/items/37cd1a417584a18cdd95)  
[Pyinstaller によるPython 3.6スクリプトのexeファイル化](https://qiita.com/jun365/items/4020ee85056f3a21c11b)  
