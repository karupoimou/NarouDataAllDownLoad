#『なろう小説API』を用いて、なろうの『全作品情報データを一括取得する』Pythonスクリプト
#2019-09-20更新
import requests
import pandas as pd
import json
import time as tm
import datetime
import gzip
from tqdm import tqdm
import re

#出力ファイル名
filename ='Narou_All_OUTPUT_09_20.xlsx'

#リクエストの秒数間隔(1以上を推奨)
interval=1

#取得するGETパラメータの「lastup」リスト
temp_lastup_list=[]   

#取得パラメータを指定
column_name_list = ['title',
                   'ncode',
                   'userid',
                   'writer',
                   'story',
                   'biggenre',
                   'genre',
                   'gensaku',
                   'keyword',
                   'general_firstup',
                   'general_lastup',
                   'novel_type',
                   'end',
                   'general_all_no',
                   'length','time',
                   'isstop',
                   'isr15',
                   'isbl',
                   'isgl',
                   'iszankoku',
                   'istensei',
                   'istenni',
                   'pc_or_k',
                   'global_point',
                   'daily_point',
                   'weekly_point',
                   'monthly_point',
                   'quarter_point',
                   'yearly_point',               
                   'fav_novel_cnt',
                   'impression_cnt',
                   'review_cnt',
                   'all_point',
                   'all_hyoka_cnt',
                   'sasie_cnt',
                   'kaiwaritu',
                   'novelupdated_at',
                   'updated_at',
                   'weekly_unique']

#####　以上設定、以下関数　##############
    
#最初に処理される関数 全体の数をメモ
def start_process():
    payload = {'out': 'json','of':'n','lim':1}
    allnum = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).text
    print('対象作品数  ',allnum);

#GETパラメータで取得する「lastup」リストを生成する
def generate_lastup_list():
    
    #現在日時の取得
    now = datetime.datetime.today()
    now_time=int(now.timestamp())
    
    #終点
    dd=datetime.datetime(2004, 1, 1, 1, 1, 1, 1)
    start_day=dd.timestamp()

    #作業経過一時保存用の変数
    unix_time = int(now.timestamp())
   
    #Unixtimeを使った期間指定で作品情報を取得する
    for i in range(100000):

        if start_day < unix_time:

            # 1日以内の投稿
            if now_time-86400 <  unix_time:
                next_time=int(unix_time-3000)

            # 約4日以内の投稿
            elif now_time-330000 <  unix_time <= now_time-86400:
                next_time=int(unix_time-8000)

            # 約十日以内の投稿
            elif now_time-1000000 <  unix_time <= now_time-250000:
                next_time=int(unix_time-12000)

            #約百日以内の投稿
            elif now_time-10000000 <  unix_time <= now_time-1000000:
                next_time=int(unix_time-25000)

            #だいぶ以前の投稿（エポック秒で直接指定していしてます）
            elif 1545000000 <  unix_time <= now_time-10000000:
                next_time=int(unix_time-40000)

            elif 1500000000 <  unix_time <= 1545000000:
                next_time=int(unix_time-80000)

            elif 1405865000 <  unix_time <= 1500000000:
                next_time=int(unix_time-100000)

            elif 1256665000 <  unix_time <= 1405865000:
                next_time=int(unix_time-200000)

            elif unix_time < 1256665000:
                next_time=int(unix_time-1000000)

            #リストに追加する
            lastup="%s-%s"%(next_time,unix_time)
            temp_lastup_list.append(lastup)
           
            #作業完了で次の取得期間を設定する
            unix_time=next_time

#全作品情報の取得
def get_all_novel_info():
    
    #レスポンスの一時リスト
    res_list=[]
    
    #リクエストエラー回数のメモ用
    error_cnt = 0 
    
    #リストを逆順にし、過去から現在に向かって取得していく        
    temp_lastup_list.reverse()
    
    #APIへリクエスト
    for lastup in tqdm(temp_lastup_list):
        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'lastup':lastup} 
        res = requests.get('https://api.syosetu.com/novelapi/api/', params=payload, timeout=10).content
        r =  gzip.decompress(res).decode("utf-8")
        
        #レスポンスを一旦リストに収納する
        res_list.append(r)
        
        #取得間隔を空ける
        tm.sleep(interval)
 
    #リクエストの展開
    dump_to_list(res_list)
        
#書き込み処理の関数
def dump_to_list(res_list):
    
    #各情報を一時的に保存していくための配列の準備
    temp_data_list=[]
    
    for i in range(len(column_name_list)):
        temp_data_list.append([])
    
    #レスポンスリストを展開
    for r in res_list:
    
        #リストに入れる
        for data in json.loads(r):
            try:
                for i in range(len(column_name_list)):               
                    temp_data_list[i].append(data[column_name_list[i]])
            except KeyError:
                pass
        
        #取れていない小説が無いか確認
        for data in json.loads(r):
            try:
                 if 500 <= data["allcount"]:
                    print("取得できなかった作品が存在します。generate_lastup_listの取得間隔を変更してください")
            except KeyError:
                pass      
            
    #エクセルファイルに書き込む処理へ        
    dump_to_excel(temp_data_list)
        
#エクセルファイルに書き込む処理
def dump_to_excel(temp_data_list):
    
    exportlist=[]
    
    #各項目のリストを1つにまとめる
    for i in range(len(column_name_list)):
        exportlist.append(temp_data_list[i])

    #pandasのデータフレームに収納 
    df = pd.DataFrame(exportlist, index=column_name_list)   
    df= df.T

    #IllegalCharacterErrorの予防
    df = df.applymap(illegal_char_remover)

    # .xlsx ファイル出力
    writer = pd.ExcelWriter(filename,options={'strings_to_urls': False})
    df.to_excel(writer, sheet_name="Sheet1")#Writerを通して書き込み
    writer.close() 

# IllegalCharacterErrorの予防、無効文字の除去
def illegal_char_remover(data):
    ILLEGAL_CHARACTERS_RE = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
    """Remove ILLEGAL CHARACTER."""
    if isinstance(data, str):
        return ILLEGAL_CHARACTERS_RE.sub("", data)
    else:
        return data

#######　関数の実行を指定　##########
print("start",datetime.datetime.now())

start_process()

generate_lastup_list()
get_all_novel_info()

print("end",datetime.datetime.now())
