import csv
import copy

def init(category_nm , msg , classtype):
	#중복제거
	category_nm = set(category_nm)
	msg = set(msg)
	classtype=set(classtype)
	msg_main=[]
	
	#msg 앞의 대분류 항목들 중복제거 
	for i in msg:
		main = i.split(" ")[0]
		msg_main.append(main)
	msg_main = set(msg_main)
	
	#msg output
	f3 = open("msg.txt","wt",encoding='UTF8')
	for i in msg:
		f3.write(i+"\n")
	f3.close()
	
	#category_nm output
	f3 = open("category.txt","wt",encoding='UTF8')
	for i in category_nm:
		
		if (i==list(category_nm)[-1]):
			f3.write(i)
		else:
			f3.write(i+"\n")
	f3.close()
	
	#msg 앞의 대분류 항목만 추출
	f3 = open("msg_main.txt","wt",encoding='UTF8')
	for i in msg_main:
		f3.write(i+"\n")
	f3.close()
	
	#classtype output
	f3 = open("classtype.txt","wt",encoding='UTF8')
	for i in classtype:
		if (i==list(classtype)[-1]):
			f3.write(i)
		else:
			f3.write(i+"\n")
	f3.close()

def col_relation(cols):
	token_classtype=[]
	token_category=[]
	relation={}

	#0열 , 2열 , 3열 , 9열 10열 csv에 다시 쓰기 
	f = open('relation.csv', 'w' ,encoding='utf-8',newline='' )
	wr = csv.writer(f)
	wr.writerow(['sid','classtype','msg', 'option' , 'msg_main' ])
	for row in cols:
		msg_main = row[2].split(" ")[0] + " " +row[2].split(" ")[-1] #msg 앞글자 뒷글자 합치기
		row.append(msg_main) 
		wr.writerow(row)
	f.close()

	cols_no_sid =[]
	for row in cols:
		row = [row[1], msg_main ] #classtype , msg_main
		cols_no_sid.append(row)

	#중복제거
	f = open('relation_deduplication.csv', 'w' ,encoding='utf-8',newline='' )
	wr = csv.writer(f)
	cols_no_sid_dedup=[]
	for i in cols_no_sid:
		if i in cols_no_sid_dedup: continue
		cols_no_sid_dedup.append(i)

	wr.writerow(['classtype','msg_main'])
	for i in cols_no_sid_dedup:
		wr.writerow(i)

def word_count(classtype_str , msg_str):
	#sid classtype msg option msg_main
	f3 = open('relation.csv', 'r', encoding='utf-8')
	rdr = csv.reader(f3)
	cnt = 0
	for line in rdr:
		if(line[1]== classtype_str):
			if msg_str in line[2]:
				cnt = cnt +1
	f3.close()
	return cnt

def word_frqcy(classtype_str):
	
	f3 = open('relation.csv', 'r', encoding='utf-8')
	rdr = csv.reader(f3)
	#msg 공백으로 나눠서 token 뽑아오기
	tokens=[]
	for line in rdr:
		msgs = line[2].split(" ")
		for msg in msgs:
			tokens.append(msg)
	tokens = set(tokens)  #token 중복 제거
	f3.close()

	#rdr이 한번쓰면 다시 못써서 다시 읽어줘야함
	f3 = open('relation.csv', 'r', encoding='utf-8')
	rdr = csv.reader(f3)

	#딕셔너리에 token넣고 값 초기화
	frqcy={}
	for token in tokens:	
		frqcy[token] = 0

	#token 개수 세기
	for line in rdr:
		if(line[1] == classtype_str):
			msgs = line[2].split(" ")
			for token in tokens:
				if token in msgs:
					frqcy[token] = frqcy[token]+1

	return frqcy
	f3.close()

def output_frqcy(classtype):
	for i in classtype:
		#\frqcy\misc-attack.csv
		f= open("./frqcy/"+i+'.csv', 'w' ,encoding='utf-8',newline='')
		wr = csv.writer(f)
		wr.writerow(["",i])
		frqcy = word_frqcy(i)

		for x,y in frqcy.items():
			wr.writerow([x,y])

