import csv
from funcs import *

f = open('0.csv', 'r', encoding='utf-8')

rdr = csv.reader(f)

cnt = 0
category_nm = []
msg = []
lines=[]
classtype=[]
cols=[] 

#read csv file 
for line in rdr:
	if(cnt==0):
		cnt=cnt+1
		lines.append(line)
	else:
		lines.append(line)
		category_nm.append(line[2])
		msg.append(line[9])
		classtype.append(line[3])
		#row = [line[0],line[2],line[3],line[9],line[10]] category_nm 삭제
		row = [line[0],line[3],line[9],line[10]]
		cols.append(row)



'''
#category_nm , msg , classtype 분류 항목들 중복제거하고 txt로 뽑기
init(category_nm , msg , classtype)
'''




#특정 열들만 뽑아서 다시 relateion.csv로 출력
col_relation(cols)





classtype = set(classtype) # 중복제거
output_frqcy(classtype) #빈도 계산해서 csv 로 결과 출력

f.close()  



