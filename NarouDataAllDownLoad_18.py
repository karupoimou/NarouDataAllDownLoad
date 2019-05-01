#『なろう１８禁API』を用いて、なろう１８禁の『全作品情報データを一括取得する』Pythonスクリプト
import requests
import pandas as pd
import json
import time as tm
import datetime
import gzip

#出力ファイル名
filename ='Narou_18_ALL_OUTPUT.xlsx'

#リクエストの秒数間隔
interval=1

#各情報を一時的に保存していくための配列
title_list=[];ncode_list=[];writer_list=[];story_list=[];nocgenre_list=[];gensaku_list=[];keyword_list=[];
general_firstup_list=[];general_lastup_list=[];novel_type_list=[];end_list=[];general_all_no_list=[];
length_list=[];time_list=[];isstop_list=[];isbl_list=[];isgl_list=[];iszankoku_list=[];istensei_list=[];
istenni_list=[];pc_or_k_list=[];global_point_list=[];fav_novel_cnt_list=[];review_cnt_list=[];all_point_list=[];
all_hyoka_cnt_list=[];sasie_cnt_list=[];kaiwaritu_list=[];novelupdated_at_list=[];updated_at_list=[];weekly_unique_list=[];

#出力の際の項目名を指定
column_name = ['title','ncode','writer','story','nocgenre','gensaku','keyword','general_firstup','general_lastup','novel_type','end','general_all_no','length','time','isstop','isbl','isgl','iszankoku','istensei','istenni','pc_or_k','global_point','fav_novel_cnt','review_cnt','all_point','all_hyoka_cnt','sasie_cnt','kaiwaritu','novelupdated_at','updated_at','weekly_unique']

#リクエストを細かく刻む用
nocgenre_set=[1,2,3,4]
type_set=['t','r','er']
kaiwa_set = ['-10','11-30','31-50','51-70','71-100']
length_set = ['-1000','1001-2000','2001-3000','3001-5000','5001-10000','10001-30000','30001-50000','50001-100000','100001-']
st_set = [1,501,1001,1501]

#処理経過数の確認用
all_process_count=0;
now_process_count=0;

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
            writer_list.append(data['writer'])
            story_list.append(data['story'])
            nocgenre_list.append(data['nocgenre'])
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
        
#最初に処理される関数
def start_process():  
    record_time('Start processing');#処理開始時刻
    payload = {'out': 'json','of':'n','lim':1}#全体の数をメモ
    all_num = requests.get('https://api.syosetu.com/novel18api/api/', params=payload).text
    print(all_num);
    
#処理の合計数を計算
def all_count():
    for nocgenre in nocgenre_set:
        for shosetu_type in type_set:
            for kaiwa in kaiwa_set:
                for leng in length_set:
                    for st in st_set:
                        global all_process_count
                        all_process_count=all_process_count+1
                        
#作品情報を取得する関数
def main_process():
    for nocgenre in nocgenre_set:
        for shosetu_type in type_set:
            for kaiwa in kaiwa_set:
                for leng in length_set:
                    for st in st_set:
                        payload = {'out':'json','gzip':5,'opt':'weekly','lim':500,'st':st,'nocgenre':nocgenre,'length':leng,'type':shosetu_type,'kaiwaritu':kaiwa} 
                        res = requests.get('https://api.syosetu.com/novel18api/api/', params=payload).content
                        r =  gzip.decompress(res).decode("utf-8")
                        dump_to_list(r);
                        global now_process_count
                        now_process_count=now_process_count+1  
                        print('step:',now_process_count,'/',all_process_count)
                        tm.sleep(interval);
                        
#######実行する関数をここで指定する##########
start_process();
all_count();
main_process();

############最終書き込み処理#################
record_time('export processing now');#処理終了時刻
exportlist=[]
exportlist.append(title_list)
exportlist.append(ncode_list)
exportlist.append(writer_list)
exportlist.append(story_list)
exportlist.append(nocgenre_list)
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
df = pd.DataFrame(exportlist, index=column_name)#pandasのデータフレームに収納 

# xlsx ファイル出力
writer = pd.ExcelWriter(filename,options={'strings_to_urls': False})
df.T.to_excel(writer, sheet_name="sheet1")#Writerを通して書き込み
writer.close()

record_time('Completed');#処理終了時刻
