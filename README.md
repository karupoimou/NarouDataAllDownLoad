# NarouDataAllDownLoad
なろう小説APIから全ての作品情報を一括取得するPythonスプリクト


## 準備
以下のパッケージを使用していますのでインストールしていない場合は導入して下さい。

pip install pandas
pip install tqdm
pip install requests

## 説明
pythonを使って、なろうAPIからすべての小説情報データを引っ張ってきて、一つの.xlsx(エクセル形式)ファイルで出力するスクリプトです。
一日動かせば、なろうのすべてが取得できます。

## 使用方法
Anacondaのjupyter notebookやPython3.5で.pyを実行してください。
実行ファイルと同じフォルダに

#出力ファイル名
filename ='All_OUTPUT.xlsx'

で指定したエクセルファイルが出力されます（ファイルサイズは約200MB）

なお出力されるまでには早くても約半日ほどかかります。
※ver2のコードでは「約90分」で全取得できるようになっています

## トラブルシューティング
### ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))
サーバーからエラーが帰って来ているということです。

リクエストの間隔をあけるためのsleep関数に使っている　datetime=1 の数字を大きくしてください。

### 「pandas」が見つからないというエラーが出る。

pip install pandas

をpipから実行してください。anacondaの場合は、スタートメニューのなかにあるanaconda promptで実行し、jupyter notebookを再起動してください。

## その他
「小説家になろう」を紹介する目的であれば使用できます。その場合、『「小説家になろう」は 
株式会社ヒナプロジェクトの登録商標です』
このスクリプトはなろう小説APIを利用するものですが非公式なものです。
