import os
import csv
from funcs import *
import urllib.parse
import base64


dirname = "./logs_3type/"
filenames = search(dirname)			
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass

json_3TypeOfdata = open('./json_3TypeOfdata.json', 'a', encoding="utf-8")

json_3TypeOfdata.write("[\n")
for file in filenames:
	f = open(dirname+file,'r',encoding='utf-8') 
	rdr = csv.reader(f)
	print("processing : " + file)
	for row in rdr:
		payload={}
		payload = tojson_3typeofdata(row[1])

		payload_str = json.dumps(payload, ensure_ascii=False, indent=4)
		payload_str+="\n,"
		json_3TypeOfdata.write(payload_str)
	f.close()

json_3TypeOfdata.write("\n{} \n]")
json_3TypeOfdata.close()