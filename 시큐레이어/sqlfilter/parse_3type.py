import os
import csv
from funcs import *
import urllib.parse
import base64
import time

dirname = "./logs_3type/"
filenames = search(dirname)			
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass

#json_3TypeOfdata = open('./json_3TypeOfdata.json', 'w', encoding="utf-8")
#json_3TypeOfdata.write("[\n")
#json_3TypeOfdata.close()

for file in filenames:
	if ".csv" in file:
		wfile = './' + file + '.json'
		json_3TypeOfdata = open(wfile, 'w', encoding="utf-8")
		json_3TypeOfdata.write("[\n")
		jsonData = ''

		f = open(dirname+file,'r',encoding='utf-8') 
		rdr = csv.reader(f)
		print("processing : " + file)
		start = time.time()
		i = 0
		for row in rdr:
			i+=1
			payload={}
			payload = tojson_single(row[1])

			payload_str = json.dumps(payload, ensure_ascii=False, indent=4)
			#jsonData += payload_str+"\n,"
			json_3TypeOfdata.write(payload_str + "\n,")

		print("%d lines, time: %s" %(i, time.time() - start))
		f.close()
		json_3TypeOfdata.write("\n{} \n]")
		json_3TypeOfdata.close()