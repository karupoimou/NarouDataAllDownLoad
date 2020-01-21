#『なろう小説API』を用いて、なろうの『全作品情報データを一括取得する』Pythonスクリプト
#2020-01-21更新
import requests
import pandas as pd
import json
import time as tm
import datetime
import gzip
from tqdm import tqdm
tqdm.pandas()
import xlsxwriter

#リクエストの秒数間隔(1以上を推奨)
interval = 1

### なろう小説API・なろう１８禁小説API を設定 ####
is_narou = True

now_day = datetime.datetime.now()
now_day = now_day.strftime("%Y_%m_%d")

if is_narou:
    filename = 'Narou_All_OUTPUT_%s.xlsx'%now_day
    api_url="https://api.syosetu.com/novelapi/api/"    
else:
    filename ='Narou_18_ALL_OUTPUT_%s.xlsx'%now_day
    api_url="https://api.syosetu.com/novel18api/api/"

#####　以上設定、以下関数　##############
    
#全作品情報の取得
def get_all_novel_info():
       
    df = pd.DataFrame()
    
    payload = {'out': 'json','gzip':5,'of':'n','lim':1}
    res = requests.get(api_url, params=payload).content
    r =  gzip.decompress(res).decode("utf-8") 
    allcount = json.loads(r)[0]["allcount"]

    print('対象作品数  ',allcount);
    
    all_queue_cnt = (allcount // 500) + 10
    
    #現在時刻を取得
    nowtime = datetime.datetime.now().timestamp()
    lastup = int(nowtime)
                     
    for i in tqdm(range(all_queue_cnt)):
        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'lastup':"1073779200-"+str(lastup)}
        
        # なろうAPIにリクエスト
        try:
            res = requests.get(api_url, params=payload, timeout=30).content
        
        # 通信エラー発生時の例外処理
        except:
            cnt=0
            while cnt < 5:
                try:
                    res = requests.get(api_url, params=payload, timeout=30).content
                    break
                except:
                    print("error")
                    cnt = cnt+1
                    tm.sleep(120) #接続エラーの場合、120秒後に再リクエストする
            
        r =  gzip.decompress(res).decode("utf-8")   
    
        # pandasのデータフレームに追加する処理
        df_temp = pd.read_json(r)
        df_temp = df_temp.drop(0)

        df = pd.concat([df, df_temp])
        
        last_general_lastup = df.iloc[-1]["general_lastup"]

        lastup = datetime.datetime.strptime(last_general_lastup, "%Y-%m-%d %H:%M:%S").timestamp()
        lastup = int(lastup)

        #取得間隔を空ける
        tm.sleep(interval)
        
    dump_to_excel(df)

#エクセルファイルに書き込む処理
def dump_to_excel(df):

    # allcount列を削除
    df = df.drop("allcount", axis=1)

    # 重複行を削除する
    df.drop_duplicates(subset='ncode', inplace=True)
    df = df.reset_index(drop=True)
    
    print("export_start",datetime.datetime.now())    

    # .xlsx ファイル出力
    writer = pd.ExcelWriter(filename,options={'strings_to_urls': False}, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1")#Writerを通して書き込み
    writer.close() 

#######　関数の実行を指定　##########
print("start",datetime.datetime.now())

get_all_novel_info()

print("end",datetime.datetime.now())
