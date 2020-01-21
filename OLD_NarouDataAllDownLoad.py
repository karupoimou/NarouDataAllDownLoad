#『なろう小説API』を用いて、なろうの『全作品情報データを一括取得する』Pythonスクリプト
#2019-08-01更新
import sys
import requests
import pandas as pd
import json
import time as tm
import datetime
import gzip
from http.client import RemoteDisconnected

#出力ファイル名
filename ='Narou_All_OUTPUT_0801.xlsx'

#リクエストの秒数間隔(1以上を推奨)
interval=1

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
               'fav_novel_cnt',
               'review_cnt',
               'all_point',
               'all_hyoka_cnt',
               'sasie_cnt',
               'kaiwaritu',
               'novelupdated_at',
               'updated_at',
               'weekly_unique']

#リスト途中経過を見るための変数
processed_num=0;

#　GETパラメータ　詳しくは「なろうディベロッパー」を参照
genre_setA = ['101','102','201','202','301','302','305','307','9999']
genre_setB = ['303','304','306','401','402','403','404']
genre_setC = ['9801']
genre_setD=['9901','9902','9903','9904']

kaiwa_setA = ['0','1-10','11-20','21-30','31-35','36-40','41-50','51-70','71-100']
length_setA = ['-250','251-400','401-450','451-500','501-600','601-700','701-1000','1001-1300','1301-1500','1501-2000','2001-3000','3001-5000','5001-7000','7001-10000','10001-13000','13001-16000','16001-20000','20001-30000','30001-50000','50001-70000','70001-100000','100001-150000','150001-200000','200001-400000','400001-500000','500001-1000000','1000001-3000000','3000001-10000000','10000001-']

kaiwa_setB = ['0','1-30','31-45','46-60','61-100']
length_setB = ['-1000','1001-10000','10001-100000','100001-']

kaiwa_setC = ['0','1-10','11-20','21-30','31-35','36-40','41-45','46-50','51-70','71-100']
length_setC = ['-199','200','201-203','204-205','206-210','211-220','221-230','231-240','241-250','251-260','261-270','271-280','281-290','291-300','301-320','321-340','341-350','351-370','371-400','401-430','431-470','471-500','501-550','551-600','601-650','651-700','701-750','751-800','801-900','901-1000','1001-1100','1101-1300','1301-1600','1601-2000','2001-2500','2501-3000','3001-3500','3501-4000','4001-5000','5001-6500','6501-8000','8001-9000','9001-10000','10001-15000','15001-20000','20001-30000','30001-40000','40001-50000','50001-100000','100001-120000','120001-200000','200001-500000','500001-1000000','1000001-']

kaiwa_setD = ['0','1-20','21-40','41-70','71-100']
length_setD = ['-199','200','201-205','206-210','211-215','216-220','221-230','231-240','241-260','261-280','281-300','301-320','321-350','351-370','371-400','401-450','451-500','501-600','601-700','701-1000','1001-1500','1501-2000','2001-3500','3501-5000','5001-20000','20001-200000','200001-']

shousetu_type_set =['t','r','er']
st_set = [1,501,1001,1501]

#時刻の書き込みに使う関数
def record_time(s):
    now = datetime.datetime.now()
    dt_now = datetime.datetime.now()
    nowtime = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    print(s+" "+nowtime)

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
            fav_novel_cnt_list.append(data['fav_novel_cnt'])
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
        
#最初に処理される関数 全体の数をメモ
def start_process():  
    record_time('Start');#処理開始時刻
    payload = {'out': 'json','of':'n','lim':1}
    allnum = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).text
    print('対象数作品  ',allnum);

#ジャンルごとに作品数を算出する関数
def genre_count(g):
    payload = {'out': 'json','of':'n','lim':1,'genre':g}
    g_num = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).text
    
    record_time('genre_start');
    
    list_length = len(title_list);
    
    global processed_num;
    
    zoubun = list_length - processed_num;
    print('前回からの増分 ',str(zoubun));
    print('現在の取得数 '+str(list_length));
    
    processed_num = list_length;#次回の計算のために現在作品数を記録
    
    print('\n対象数作品  ',g_num);#次ジャンルの作品総数を表示

    
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

# STの計算に使う
def check_st(payload):
    
    allcount=[] 
    res = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).content
    r =  gzip.decompress(res).decode("utf-8")
    
    for data in json.loads(r):
        try:            
            allcount.append(data['allcount'])
        except KeyError:
            pass
        
    print(allcount[0])

    if allcount[0]<500:
        return 1;
    elif 500<=allcount[0]<1000:
        return 2;
    else:
        return 4;
    
#多いジャンルの作品情報を取得する関数    
def genre_A():
    for gen in genre_setA:
        genre_count(gen);#開始時間　ジャンル内の作品数を記録

        for kai in kaiwa_setA:                
            for leng in length_setA:
                for sho in shousetu_type_set:
                    
                    print(gen+" "+kai+" "+leng+" "+sho)#進行状況の表示
                    payload = {'out': 'json','gzip':5,'lim':1,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho}
                    st_num=check_st(payload)
                    
                    for s in range(st_num):                        
                        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'genre':gen,'kaiwaritu':kai,'length':leng,'st':st_set[s],'type':sho}
                        requests_to_api(payload);
                        
#少ないジャンルの作品情報を取得する関数    
def genre_B():
    for gen in genre_setB:
        genre_count(gen);#開始時間　ジャンル内の作品数を記録   
       
        for kai in kaiwa_setB:
            for leng in length_setB:
                for sho in shousetu_type_set:

                    print(gen+" "+kai+" "+leng+" "+sho)#進行状況の表示
                    payload = {'out': 'json','gzip':5,'lim':1,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho}
                    st_num=check_st(payload)
                    
                    for s in range(st_num): 
                        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho,'st':st_set[s]}
                        requests_to_api(payload);
                   
                    
#『ノンジャンル：9801』の作品情報を取得する関数 
def genre_C():
    for gen in genre_setC:
        genre_count(gen);#開始時間　ジャンル内の作品数を記録

        for kai in kaiwa_setC:
            for leng in length_setC:
                for sho in shousetu_type_set:
                    
                    print(gen+" "+kai+" "+leng+" "+sho)#進行状況の表示
                    payload = {'out': 'json','gzip':5,'lim':1,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho}
                    st_num=check_st(payload)
                    
                    for s in range(st_num):
                        payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho,'st':st_set[s]}
                        requests_to_api(payload);
                        
#99XXジャンルを取得する関数
def genre_D():
    for gen in genre_setD:
        genre_count(gen);#開始時間　ジャンル内の作品数を記録
        
        if gen=='9904':#リプレイジャンルのみ数が少ないので飛ばす
            for sts in st_set:
                print(gen)#進行状況の表示

                payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'genre':gen,'st':sts}
                res = requests.get('https://api.syosetu.com/novelapi/api/', params=payload).content
                r =  gzip.decompress(res).decode("utf-8")
                dump_to_list(r);
                tm.sleep(interval); 
        else:
            for kai in kaiwa_setD:                
                for leng in length_setD:

                    for sho in shousetu_type_set:
                        print(gen+" "+kai+" "+leng+" "+sho)#進行状況の表示
                        payload =  {'out': 'json','gzip':5,'lim':1,'genre':gen,'kaiwaritu':kai,'length':leng,'type':sho}
                        st_num=check_st(payload)
                        
                        for s in range(st_num):
                            payload = {'out': 'json','gzip':5,'opt':'weekly','lim':500,'genre':gen,'kaiwaritu':kai,'length':leng,'st':st_set[s],'type':sho}
                            requests_to_api(payload);


#書き込み処理
def dump_to_excel():
    record_time('start export processing');#最終処理開始時刻
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
    exportlist.append(fav_novel_cnt_list)
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

    # .xlsx ファイル出力
    writer = pd.ExcelWriter(filename,options={'strings_to_urls': False})
    df.T.to_excel(writer, sheet_name="sheet1")#Writerを通して書き込み
    writer.close()

#######実行する関数をここで指定する##########

#必要がないものはコメントアウトしてください
#また分割して取得する際にご利用ください
t1 = tm.time()

start_process();
genre_A();
genre_B();
genre_C();
genre_D();

dump_to_excel()

t2 = tm.time()

record_time('Completed');#処理終了時刻
print("処理に掛かった時間："+str(t2-t1)+"秒")
