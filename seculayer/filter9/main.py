import os
import csv
from filter import *


dirname = "./log/"
filenames = search(dirname)		

OX_file = "XO_index.txt"
RawData_file = "rawdata_index.txt"
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass

for file in filenames:

	if "csv" not in file:

		continue

	OX_IndexDict = read_IndexFile(OX_file)
	Rawdata_IndexDict = read_IndexFile(RawData_file)

	OX_index = OX_IndexDict[file]
	Rawdata_index = Rawdata_IndexDict[file]

	#정탐오탐여부가 엑셀안에 칼럼이 잇을때
	if( OX_index != -1):
		f = open(dirname+file,'r',encoding='utf-8') 
		rdr = csv.reader(f)
	
	
		output_correct = open("output/"+file+"_정탐.txt","a",encoding="utf-8")
		output_wrong = open("output/"+file+"_오탐.txt","a",encoding="utf-8")

		output_correct_with_rawdata = open("output/"+file+"_정탐_원본포함.txt","a",encoding="utf-8")
		output_wrong_with_rawdata = open("output/"+file+"_오탐_원본포함.txt","a",encoding="utf-8")
		
		output_len_correct = open("output_len/"+file+"_정탐_Length.txt","a",encoding="utf-8")
		output_len_wrong = open("output_len/"+file+"__오탐_Length.txt","a",encoding="utf-8")
	
		output_word_correct = open("output_word/"+file+"_정탐_word.txt","a",encoding="utf-8")
		output_word_wrong = open("output_word/"+file+"_오탐_word.txt","a",encoding="utf-8")
	
	
	
		atk_type = check_atktype(file)
	
		
		count = 1
		print("processing : ",file,"   Attack Type : ",atk_type , " rawdata index : ", Rawdata_index , "OX_index : ",OX_index)
		for row in rdr:
		
			if( row[OX_index]==str(1)):
	
				#filter함수를 통해 [a,b,c]형태로 만든후 그것을 filter_list에 대입
				filter_list = filter(row[Rawdata_index],atk_type,count)		
	
				#중복제거
				filter_list = list(set(filter_list))	
	
	
				#output폴더에 결과 출력 
				output_correct.write(str(filter_list)+"\n")	
	
				output_correct_with_rawdata.write(str(filter_list)+" , "+row[Rawdata_index]+"\n")
				#output_len폴더에 결과출력`
				filter_list_len = List2length(filter_list)
				output_len_correct.write(str(filter_list_len)+"\n")
	
				#word만 뽑기
				filter_list = Word_only(filter_list)
	
	
				#output_word에 결과출력
				output_word_correct.write(str(filter_list)+"\n")
	
	
			elif( row[OX_index]==str(0)):
				filter_list = filter(row[Rawdata_index],atk_type,count)		
				#중복제거
				filter_list = list(set(filter_list))
	
				#output폴더에 결과 출력 
				output_wrong.write(str(filter_list)+"\n")	
				output_wrong_with_rawdata.write(str(filter_list)+" , "+row[Rawdata_index]+"\n")

				#output_len폴더에 결과출력
				filter_list_len = List2length(filter_list)
				output_len_wrong.write(str(filter_list_len)+"\n")
	
				#word만 뽑기
				filter_list = Word_only(filter_list)
	
	
				#output_word에 결과출력
				output_word_wrong.write(str(filter_list)+"\n")
			count +=1
	
	
	
		output_correct.close()
		output_wrong.close()
	
		output_len_correct.close()
		output_len_wrong.close()
	
		output_word_correct.close()
		output_word_wrong.close()
	
		f.close()
	#정탐오탐여부가 엑셀안에 칼럼이 없고 애초에 구분되어있을때

	else:
		f = open(dirname+file,'r',encoding='utf-8') 
		rdr = csv.reader(f)
	
		
		output = open("output/"+file+".txt","a",encoding="utf-8")
		output_with_rawdata = open("output/"+file+"_원본포함.txt","a",encoding="utf-8")
		output_word = open("output_word/"+file+"_word.txt","a",encoding="utf-8")
		output_len = open("output_len/"+file+"_Length.txt","a",encoding="utf-8")
	
		atk_type = check_atktype(file)
		print("processing : ",file,"   Attack Type : ",atk_type)
		count = 1
		for row in rdr:
			filter_list = filter(row[Rawdata_index],atk_type,count)		
	
			#중복제거
			filter_list = list(set(filter_list))
	
			#output폴더에 결과 출력 
			output.write(str(filter_list)+"\n")	
			output_with_rawdata.write(str(filter_list)+" , "+row[Rawdata_index]+"\n")

			#output_len폴더에 결과출력
			filter_list_len = List2length(filter_list)
			output_len.write(str(filter_list_len)+"\n")
	
			#word만 뽑기
			filter_list = Word_only(filter_list)
	
			#output_word에 결과출력
			output_word.write(str(filter_list)+"\n")
			count+=1
		output.close()
		output_word.close()
		output_len.close()
		f.close()
		


'''


#kisa level 1 외의 파일들 파싱용 
dirname = "./log/"
filenames = search(dirname)		
#file = "level1.kisa.sql_injection_total_shuffled.csv"	
RawData_file = "rawdata_index.txt"
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass


for file in filenames:

	if "csv" not in file:
		continue

	f = open(dirname+file,'r',encoding='utf-8') 
	rdr = csv.reader(f)

	
	output = open("output/"+file+".txt","a",encoding="utf-8")
	output_word = open("output_word/"+file+"_word.txt","a",encoding="utf-8")
	output_len = open("output_len/"+file+"_Length.txt","a",encoding="utf-8")

	atk_type = check_atktype(file)
	Rawdata_IndexDict = read_IndexFile(RawData_file)
	index = Rawdata_IndexDict[file]

	print("processing : ",file,"   Attack Type : ",atk_type)
	for row in rdr:
		filter_list = filter(row[index],atk_type)		

		#중복제거
		filter_list = list(set(filter_list))

		#output폴더에 결과 출력 
		output.write(str(filter_list)+"\n")	

		#output_len폴더에 결과출력
		filter_list_len = List2length(filter_list)
		output_len.write(str(filter_list_len)+"\n")

		#word만 뽑기
		filter_list = Word_only(filter_list)

		#output_word에 결과출력
		output_word.write(str(filter_list)+"\n")

	output.close()
	output_word.close()
	output_len.close()
	f.close()
'''