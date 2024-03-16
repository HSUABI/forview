import os
import csv
from funcs import *
import urllib.parse
import base64



paystr2json = open('paystr2json.json', 'a', encoding="utf-8")	#paystr2json.json 에다가 csv데이터  json형식으로 저장
paystr2json.write("[\n")
f = open("./logs/LOG_admin_20181116151221_ok.csv",'r',encoding='utf-8') 
rdr = csv.reader(f)
print("processing : " + "LOG_admin_20181116151221_ok.csv")
check = 0							#엑셀 첫행 체크용 변수 
for row in rdr:
	file_data={}
	try:
		if check==0:	#엑셀 첫행 건너뛰기 용
			check+=1
			continue
		#json.dump 하면 이스케이프문자 그대로 덤프되서 이렇게 일일히 다써줌
		paystr2json.write("{")
		paystr2json.write('\n\t"PAYLOAD":' +'[')
		payload_json_bunch = pay2json( row[11].replace("\r\n","\n") ,"정탐-전체페이로드1.csv" )		#한칸에 GET POS몰려서 적혀있을경우 패킷이 여러개있어서 bunch라고 이름지음
		paystr2json.write(payload_json_bunch)	
		paystr2json.write(']')
		paystr2json.write("\n},\n")

	except IndexError:			#12110301_12110500_ok.csv 에 공백열이잇다. 그래서 예외처리
		pass
paystr2json.write("\n{} \n]")
paystr2json.close
f.close()
