import os
import csv
from funcs import *
import urllib.parse
import base64
import time
from sql_filter import *
from join import *


'''
name = "test.json"
f=open(name,"r",encoding="utf-8")

data = json.load(f)

for i in data:
	for j in i["DATA"]:
		
		string = base64.b64decode(j).decode("utf-8")
		sql = string.split()
		print(string)
		parse(sql)
		print("")
	print("-----")
'''
name = "join_example"
f=open(name,"r",encoding="utf-8")
lines = f.readlines()
for line in lines:
	if "//" in line:
		continue

	a = join_parse(line.lower())
	string = a
	print(line)
	print(a)
	print(a.replace("space!@#"," "))
	
	#sql = string.split()
	#sql = parse(sql)
	print("-----")
