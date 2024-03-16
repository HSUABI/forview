import os
import csv
from funcs import *
from tknize import *
from filter import *
import urllib.parse
import base64
import time
import ast


dirname = "./output/"
filenames = search(dirname)		
#file = "level1.kisa.sql_injection_total_shuffled.csv"	

try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass


for file in filenames:

	if "txt" not in file:
		continue
	f = open(dirname+file,'r',encoding='utf-8') 
	lines = f.read().split("\n")
	output_len = open("output_len/"+file[:-4]+"_Length.txt","a",encoding="utf-8")

	print("processing : ",file)
	for line in lines:

		if "" in line : #맨끝이면 패스
			continue

		try:
			list = ast.literal_eval(line)
			list = List2length(list)
			output_len.write(str(list)+"\n")
		except:
			print("error : "+line)


	output_len.close()
	f.close()