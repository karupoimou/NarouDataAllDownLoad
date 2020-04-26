# 概要
なろう小説APIから全ての作品情報を一括取得するPythonスプリクト

## 説明
pythonを使って「なろうAPI」からなろうに存在する全ての小説情報データを引っ張ってきて、一つの.xlsx(エクセル形式)ファイルで出力するスクリプトです。

なろう版は約90分、ノク・ムン・ミッド版は約7分動かせば、なろうの全てが取得できます。

## 使用準備
以下のpipパッケージを使用していますのでインストールしていない場合は導入して下さい。
```
pip install pandas
pip install tqdm
pip install requests
pip install xlsxwriter
```

## 使用方法
Python3.5以上のバージョンで.pyを実行してください。
実行ファイルと同じフォルダに
```
#出力ファイル名
filename ='All_OUTPUT_20xx_xx_xx.xlsx'
```
で指定したエクセルファイルが出力されます（なおファイルサイズは約200MBです）

## トラブルシューティング
### ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
サーバーからエラーが帰って来ているということです。

リクエストの間隔をあけるためのsleep関数に使っている「interval=1」の数字を大きくしてください。

### 「pandas」が見つからないというエラーが出る。

`pip install pandas`

をpipから実行してください。anacondaの場合は、スタートメニューのなかにあるanaconda promptで実行し、jupyter notebookを再起動してください。

## その他
・株式会社ヒナプロジェクトの登録商標です
・このスクリプトはなろう小説APIを利用するものですが非公式なものです。
