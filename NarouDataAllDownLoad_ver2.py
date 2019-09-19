#『なろう小説API』を用いて、なろうの『全作品情報データを一括取得する』Pythonスクリプト
#2019-09-20更新
import sys
import requests
import pandas as pd
import json
import time as tm
import datetime
import gzip
from tqdm import tqdm
from http.client import RemoteDisconnected
import openpyxl
import re

#出力ファイル名
filename ='Narou_All_OUTPUT_09_20.xlsx'

#リクエストの秒数間隔(1以上を推奨)
interval=1

#取得するGETパラメータの「lastup」リスト
temp_lastup_list=[]

#各情報を一時的に保存していくための配列
title_list=[]
ncode_list=[]
userid_list=[]
writer_list=[]
story_list=[]
biggenre_list=[]
genre_list=[]
gensaku_list=[]
keyword_list=[]
general_firstup_list=[]
general_lastup_list=[]
novel_type_list=[]
end_list=[]
general_all_no_list=[]
length_list=[]
time_list=[]
isstop_list=[]
isr15_list=[]
isbl_list=[]
isgl_list=[]
iszankoku_list=[]
istensei_list=[]
istenni_list=[]
pc_or_k_list=[]
global_point_list=[]
fav_novel_cnt_list=[]
review_cnt_list=[]
all_point_list=[]
all_hyoka_cnt_list=[]
sasie_cnt_list=[]
kaiwaritu_list=[]
novelupdated_at_list=[]
updated_at_list=[]
weekly_unique_list=[]

#追加2019_08_26
daily_point_list=[]
weekly_point_list=[]
monthly_point_list=[]
quarter_point_list=[]
yearly_point_list=[]
impression_cnt_list=[]

#出力の際の項目名を指定
column_name = ['title',
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
               'end','general_all_no',
               'length','time','isstop',
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

#最初に処理される関数 全体の数をメモ
def start_process():
    payload = {'out': 'json','of':'n','lim':1}
    allnum = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).text
    print('対象数作品  ',allnum);

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
        
            #数日以内の投稿
            if now_time-100000 <  unix_time:
                next_time=int(unix_time-2000)

            #数十日以内の投稿
            elif now_time-1000000 <  unix_time <= now_time-100000:
                next_time=int(unix_time-5000)

            #数百日以内の投稿
            elif now_time-10000000 <  unix_time <= now_time-1000000:
                next_time=int(unix_time-20000)
            
            #だいぶ以前の投稿（エポック秒で直接指定していしてます）
            elif 1545000000 <  unix_time <= now_time-10000000:
                next_time=int(unix_time-30000)
                
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
    
    #リストを逆順にし、過去から現在に向かって取得していく        
    temp_lastup_list.reverse()
    
    for lastup in tqdm(temp_lastup_list):
        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'lastup':lastup}
        requests_to_api(payload)
        
#　APIにリクエストを行い、データを受け取る。RemoteDisconnectedの場合は60秒を置いて10回までトライする
def requests_to_api(payload):
    
    i = 0  
    
    while i < 10:
        try:
            res = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).content
            break

        except RemoteDisconnected:
            print("RemoteDisconnected Error! Waiting for reload")
            tm.sleep(60)
            i=i+1
            if i == 10:
                print("RemoteDisconnected Error. Incomplete.　Sys exit")
                sys.exit()
            else:
                pass
            
    r =  gzip.decompress(res).decode("utf-8")
    dump_to_list(r);                    

    tm.sleep(interval);

#書き込み処理の関数
def dump_to_list(r):
    for data in json.loads(r):
        try:            
            title_list.append(data['title'])
            ncode_list.append(data['ncode'])
            userid_list.append(data['userid'])
            writer_list.append(data['writer'])
            story_list.append(data['story'])
            biggenre_list.append(data['biggenre'])
            genre_list.append(data['genre'])
            gensaku_list.append(data['gensaku'])
            keyword_list.append(data['keyword'])
            general_firstup_list.append(data['general_firstup'])
            general_lastup_list.append(data['general_lastup'])
            novel_type_list.append(data['novel_type'])
            end_list.append(data['end'])
            general_all_no_list.append(data['general_all_no'])
            length_list.append(data['length'])
            time_list.append(data['time'])
            isstop_list.append(data['isstop'])
            isr15_list.append(data['isr15'])
            isbl_list.append(data['isbl'])
            isgl_list.append(data['isgl'])
            iszankoku_list.append(data['iszankoku'])
            istensei_list.append(data['istensei'])
            istenni_list.append(data['istenni'])
            pc_or_k_list.append(data['pc_or_k'])
            global_point_list.append(data['global_point'])            
            daily_point_list.append(data['daily_point'])#追加2019_08_26
            weekly_point_list.append(data['weekly_point'])#追加2019_08_26
            monthly_point_list.append(data['monthly_point'])#追加2019_08_26
            quarter_point_list.append(data['quarter_point'])#追加2019_08_26
            yearly_point_list.append(data['yearly_point'])#追加2019_08_26
            fav_novel_cnt_list.append(data['fav_novel_cnt'])
            impression_cnt_list.append(data['impression_cnt'])#追加2019_08_26            
            review_cnt_list.append(data['review_cnt'])
            all_point_list.append(data['all_point'])
            all_hyoka_cnt_list.append(data['all_hyoka_cnt'])
            sasie_cnt_list.append(data['sasie_cnt'])
            kaiwaritu_list.append(data['kaiwaritu'])
            novelupdated_at_list.append(data['novelupdated_at'])
            updated_at_list.append(data['updated_at'])
            weekly_unique_list.append(data['weekly_unique'])
        except KeyError:
            pass
        
#書き込み処理
def dump_to_excel():
    exportlist=[]
    exportlist.append(title_list)
    exportlist.append(ncode_list)
    exportlist.append(userid_list)
    exportlist.append(writer_list)
    exportlist.append(story_list)
    exportlist.append(biggenre_list)
    exportlist.append(genre_list)
    exportlist.append(gensaku_list)
    exportlist.append(keyword_list)
    exportlist.append(general_firstup_list)
    exportlist.append(general_lastup_list)
    exportlist.append(novel_type_list)
    exportlist.append(end_list)
    exportlist.append(general_all_no_list)
    exportlist.append(length_list)
    exportlist.append(time_list)
    exportlist.append(isstop_list)
    exportlist.append(isr15_list)
    exportlist.append(isbl_list)
    exportlist.append(isgl_list)
    exportlist.append(iszankoku_list)
    exportlist.append(istensei_list)
    exportlist.append(istenni_list)
    exportlist.append(pc_or_k_list)
    exportlist.append(global_point_list)
    exportlist.append(daily_point_list)#追加2019_08_26  
    exportlist.append(weekly_point_list)#追加2019_08_26  
    exportlist.append(monthly_point_list)#追加2019_08_26  
    exportlist.append(quarter_point_list)#追加2019_08_26  
    exportlist.append(yearly_point_list)#追加2019_08_26  
    exportlist.append(fav_novel_cnt_list)    
    exportlist.append(impression_cnt_list)#追加2019_08_26      
    exportlist.append(review_cnt_list)
    exportlist.append(all_point_list)
    exportlist.append(all_hyoka_cnt_list)
    exportlist.append(sasie_cnt_list)
    exportlist.append(kaiwaritu_list)
    exportlist.append(novelupdated_at_list)
    exportlist.append(updated_at_list)
    exportlist.append(weekly_unique_list)

    #pandasのデータフレームに収納 
    df = pd.DataFrame(exportlist, index=column_name)
    
    #重複行の削除
    df = df.T.drop_duplicates(subset='ncode')

    #IllegalCharacterErrorの予防
    df = df.applymap(illegal_char_remover)

    # .xlsx ファイル出力
    writer = pd.ExcelWriter(filename,options={'strings_to_urls': False})
    df.to_excel(writer, sheet_name="Sheet1")#Writerを通して書き込み
    writer.close() 

# IllegalCharacterErrorの予防 無効文字の除去
def illegal_char_remover(data):
    ILLEGAL_CHARACTERS_RE = re.compile(
        r'[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]')
    """Remove ILLEGAL CHARACTER."""
    if isinstance(data, str):
        return ILLEGAL_CHARACTERS_RE.sub("", data)
    else:
        return data

#######実行する関数をここで指定する##########
start_process()

generate_lastup_list()
get_all_novel_info()

dump_to_excel()

print("end")
