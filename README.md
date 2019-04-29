# NarouDataAllDownLoad
なろう小説APIから全ての作品情報を一括取得するPythonスプリクト


## 準備
pandasパッケージを使用していますのでインストールしていない場合は導入して下さい。

pip install pandas

## 説明
pythonを使って、なろうAPIからすべての小説情報データを引っ張ってきて、一つの.xlsx(エクセル形式)ファイルで出力するスクリプトです。
一日動かせば、なろうのすべてが取得できます。

## 使用方法
Anacondaのjupyter notebookやPython3.5で.pyを実行してください。
実行ファイルと同じフォルダに

#出力ファイル名
filename ='All_OUTPUT.xlsx'

で指定したエクセルファイルが出力されます。

なお出力されるまでには早くても約半日ほどかかります。

### 分割してデータを取得する方法
コードの下の方に「実行する関数をここで指定する」というとこにある。

major_genre();
minor_genre();
non_genre();

のコードを適宜コメントアウトすることで、ファイルを一つにまとめずに、１つずつ分けて取得する事もできます。
一度に全部落とそうとすると長時間かかるためサーバーエラーにあう確率が上がります。なので、その様な場合は分割してデータを取得してみてください。

## トラブルシューティング
###ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
サーバーからエラーが帰って来ているということです。

リクエストの間隔をあけるためのsleep関数に使っている　datetime=1 の数字を大きくしてください。

###「pandas」が見つからないというエラーが出る。

pip install pandas

をpipから実行してください。anacondaの場合は、スタートメニューのなかにあるanaconda promptで実行し、jupyter notebookを再起動してください。
