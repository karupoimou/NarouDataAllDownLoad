# NarouDataAllDownLoad
なろうAPIから全ての作品情報を一括取得するPythonスプリクト


準備
pandasパッケージを使用していますのでインストールしていない場合は導入して下さい。

pip install pandas

説明
pythonを使って、なろうAPIからすべての小説情報データを引っ張ってきて、一つの.xlsx(エクセル形式)ファイルで出力するスクリプトです。
一日動かせば、なろうのすべてが取得できます。

トラブルシューティング
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
サーバーからエラーが帰って来ているということです。

リクエストの間隔をあけるためのsleep関数に使っている　datetime=1 の数字を大きくしてください。
