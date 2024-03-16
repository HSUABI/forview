#-*- coding: utf-8 -*-
'''
필독 : 돌리기전에 csv파일 무조건 utf로 저장하기 하고 해야함
'''
import os
import csv
from funcs import *
import urllib.parse
import base64


dirname = "./logs/"
#파일마다 열순서가 다르다 그래서 특정 문자가 몇번째 열에잇는지 구하는것
time_index = index_dict("장비발생시간",dirname)
sip_index = index_dict("출발지IP",dirname)
sport_index = index_dict("출발지포트",dirname)
dip_index = index_dict('목적지IP',dirname)
dport_index = index_dict("목적지포트",dirname)
msg_index = index_dict('공격명',dirname)
payload_index = index_dict('페이로드',dirname)
proto_index = index_dict("프로토콜",dirname)
res_index={}
res_index.update(index_dict('정오탐',dirname))
res_index.update(index_dict('결과',dirname))

csvtojson = open('csvtojson.json', 'a', encoding="utf-8")	#csvtojson.json 에다가 csv데이터  json형식으로 저장

filenames = search(dirname)			
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass
csvtojson.write("[\n")
for file in filenames:
	f = open(dirname+file,'r',encoding='utf-8') 
	rdr = csv.reader(f)
	print("processing : " + file)
	check = 0							#엑셀 첫행 체크용 변수 
	for row in rdr:
		file_data={}
		try:
			if check==0:	#엑셀 첫행 건너뛰기 용
				check+=1
				continue
			#json.dump 하면 이스케이프문자 그대로 덤프되서 이렇게 일일히 다써줌
			csvtojson.write("{")
			csvtojson.write('\n\t"TIME": '+'"'+row[time_index[file]]+'",' )	#"TIME": "2018-12-08 5:01"
			csvtojson.write('\n\t"SIP": '+'"'+row[sip_index[file]]+'",' )
			csvtojson.write('\n\t"SPORT": '+'"'+row[sport_index[file]]+'",' )
			csvtojson.write('\n\t"DIP": '+'"'+row[dip_index[file]]+'",' )
			csvtojson.write('\n\t"DPORT": '+'"'+row[dport_index[file]]+'",' )
			csvtojson.write('\n\t"MSG": '+'"'+row[msg_index[file]]+'",' )
			csvtojson.write('\n\t"RES": '+'"'+row[res_index[file]]+'",' )
			csvtojson.write('\n\t"PAYLOAD":' +'[')
			payload_json_bunch = pay2json( row[payload_index[file]] ,file )		#한칸에 GET POS몰려서 적혀있을경우 패킷이 여러개있어서 bunch라고 이름지음
			csvtojson.write(payload_json_bunch)	
			csvtojson.write(']')
			csvtojson.write("\n},\n")
            
		except IndexError:			#12110301_12110500_ok.csv 에 공백열이잇다. 그래서 예외처리
			pass

	f.close()

csvtojson.write("\n{} \n]")
csvtojson.close()