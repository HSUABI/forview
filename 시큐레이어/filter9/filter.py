import os
import csv
import json 
import urllib.parse
import base64
import time
import copy


'''
funcs.py에서 사용하는 함수들만 가져옴
'''
def search(dirname):
	filenames = os.listdir(dirname)
	return filenames
	
def strcat(token2): # 파라미터에 = 들어갔을경우 예외처리
	str_=''
	for i in token2[1:]:		
		if(i==token2[-1]):	#id=1%20and%201=2%20union 이럴때 "1=2" 넣기위함
			str_ +=i
		else:				# 맨마지막에 =붙이면안됨
			str_+= (i+"=")
	return str_

def parseparam(params,count):
	ret = ''
	tokens = params.split("&") #channel=cd5e2516 & version=5.5.7.0
	arr=[]
	if len(tokens) == 1:		#인자 1개일때 ex)/jexws3/jexws3.jsp?ppp=echo%20Hello%20D3c3mb3r
		token2=tokens[0].split("=")
		if len(token2) >1:
			str_=strcat(token2)

			#base64로 만들기
			str_urldecode = urllib.parse.unquote(str_)
			str_base64 = base64.b64encode(str_urldecode.encode("utf-8")).decode("utf-8")
			arr.append(str_base64)
	else:						# &로 인자가 2개이상일경우
		for token in tokens:
			token2=token.split("=")
			if len(token2) ==1:
				continue
			str_=strcat(token2)

			#base64로 만들기
			str_urldecode = urllib.parse.unquote(str_)
			str_base64 = base64.b64encode(str_urldecode.encode("utf-8")).decode("utf-8")
			arr.append(str_base64)
	return arr

def parsejson(json):	#{"success":false,"error":"error name1", "code":1} 이런거 파싱
	arr=[]
	tokens = json.split(",")	# ,으로 나눈다. 예 : "success":false
	if len(tokens) == 1:
		token2 = tokens[0].split(":")	# :으로 나눈다 예 : false
		if len(token2) > 1:
			str_ = token2[1].replace('"',"")	# "test" 같은 거를 test로 만들어주기

			#base64
			str_urldecode = urllib.parse.unquote(str_)
			str_base64 = base64.b64encode(str_urldecode.encode("utf-8")).decode("utf-8")
			arr.append(str_base64)
	else:
		for token in tokens:
			token2 = token.split(":")
			if len(token2) ==1:
				continue
			str_ = token2[1].replace('"',"")

			#base64
			str_urldecode = urllib.parse.unquote(str_)
			str_base64 = base64.b64encode(str_urldecode.encode("utf-8")).decode("utf-8")
			arr.append(str_base64)

	return arr

def parsecookie(cookies): #parseparam과 거의 동일하나 &대신 ;로 나눔
	ret = ''
	tokens = cookies.split(";") #uid=410482; ssotoken=Vy3zFyENGI
	arr=[]
	if len(tokens) == 1:		#인자 1개일때 ex)uid=410482
		token2=tokens[0].split("=")
		if len(token2) >1:
			str_=strcat(token2)
			arr.append(str_)
	else:						# ;로 인자가 2개이상일경우
		for token in tokens:
			token2=token.split("=")
			if len(token2) ==1:
				continue
			str_=strcat(token2)
			arr.append(str_)
	return arr

#key는대문자 data는 소문자임!!
def payload_add(string , token):	#URL , Host , UserAgent 등등이 인자로 들어감
	payload={}						#parePOST의 postbody와 같은 역할

	#request "Cookie : xxx" 와 response의 "Set-Cookie: JSESSIONID=jZ0b5v~~`"를 다 커버하는 코드임
	if string in token[:len(string)+2] and string == "COOKIE:":
		cookies = token.split(":", maxsplit=1)[1]
		cookie_list = parsecookie(cookies)
		payload["COOKIE"] = cookie_list

	elif(string in token[:len(string)+2]):
		# "Host: " --> "HOST"
		token2 = token.split(":", maxsplit=1)
		payload[token2[0].upper()] = token2[1].lower()

	return payload


'''
tknize.py 함수
'''
def Word_only(data):
	data_only_word=[]
	word=""
	for string in data:	#string은 ["abc","ddd"]에서 abc와 ddd를 의미 

		for character in string:	#character는 "abc"를 탐색한다 가정할때 a" "b" "c"를 의미 
			if character.isalpha() == True:
				word += character
			elif character =="%":	#U%N%I%O%N 이런것들 고려
				continue
			elif character.isalpha() == False:
				data_only_word.append(word)
				word = ""
		#['soccer', "htm');", '201904', "javascript:PrintOpen('", 'sp2019040515465393750', 'lpage'] 이런경우일때는
		#리스트에서 하나의 원소가 끝났을시에 word를 append해줘야한다. 이걸하지않으면
		#['soccerhtm', 'javascript', 'PrintOpen', 'sp'] 이렇게 되어버린다.
		data_only_word.append(word)
		word = ""

	#리스트에 공백 들어가는거 색제
	DATA_for_search = data_only_word[:]	#탐색용 배열 
	for i in DATA_for_search:
		if i =="":
			data_only_word.remove("")
	return data_only_word

def URL_word(url):
	# '/' '\' 이런거 한꺼번에 split해주기
	url_only_word=[]

	URL = url
	URL = URL.replace("/","split_word")
	URL = URL.replace("\\","split_word")
	url_only_word = URL.split("split_word")		

	file = url_only_word[-1]	#/abc/acb/file.txt , url에서 file.txt를 가져오는거
	file = file.split(".")

	#file.txt를 file , txt로 나누기
	del url_only_word[-1]
	url_only_word = url_only_word + file

	#DATA에 공백 들어가는거 색제
	DATA_for_search = url_only_word[:]	#탐색용 배열 
	for i in DATA_for_search:
		if i =="":
			url_only_word.remove("")
	return url_only_word





'''
파싱 도움 함수들
'''
def check_DataType(line,count=1):

	line = line.upper()
	tokens = line.upper().split('\n')
	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":'',\
				"DATA_MUTITYPE_LENGTH":[], "DATA_MUTITYPE_CONTENT-TYPE":[]}

	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		payload.update(payload_add("REFERER:",token))
		payload.update(payload_add("USER-AGENT:",token))

		if payload["CONTENT-TYPE"] == '':	#multipart 파싱할때 content-type을 multipart의 content type으로 덮어쓰는경우를 방지. FU(Train.csv) 1037라인 같은곳에서 파싱이 잘안됨
			payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))

	#SQL PARAM 50 파일에 있는데이터 예외처리
	if "getPortal".lower() in line.lower():
		return 31

	if line=="":	#rawdata칸에 아무것도없으면
		return -1

	if line[0] == '/': 

		#정상패킷인데 앞에 GET , POST 같은 메소드이름만 없을떄
		for value in payload.values():
			if not (value ==[] or value ==''):
				return 12

		#딱 url부분만 있을떄
		return 11

	elif "GET" in line[:4] or "POST" in line[:4] \
			or "HTTP/1.1" in line[:10] or "HTTP/1.0" in line[:10] :
		return 2

	else:
		for value in payload.values():
			if not (value ==[] or value ==''):
				return 32

		return 31

def decode_base64(list):
	dummy = []

	for i in list:
		dummy.append(base64.b64decode(i).decode("utf-8"))

	return dummy

def encode_list(list):
	dummy = []

	for i in list:
		dummy.append(base64.b64encode(i.encode("utf-8")).decode("utf-8"))


	return dummy
def read_IndexFile(file):
	
	f = open(file,"r",encoding="utf-8")
	index_dict = json.load(f)
	
	return index_dict

# list에는 filter_parse_type_# 함수를 통해나온 리스트를 받는다.
def mk_result(list,datatype):
	a = list
	try:
		#b=decode_base64(a)
		b=a
		f2= open("test"+str(datatype)+".txt","a",encoding="utf-8")
		f2.write(str(b)+"\n")
		f2.close()
	except:
		print("error"+str(datatype)+"2: "+line)
		pass




'''
기존에는 딕셔너리를 만들었음
이제는 태깅이된걸 보고 필요한부분만 파싱해서리턴

함수 인풋 : 공격유형 , rawdata
함수 아웃풋 : 리스트

* 뽑아야할것 

1. CSRF
	- DATA, URL COOKIE
	
2. XSS
	- DATA, URL COOKIE

3. SQL
	- DATA, REFERER

4. UAA(경로추적)
	- URL

5. 운영체제(cmd, bash)
	- DATA

6. 자동화 공격, 정상 User-Agent 리스트 수집, (ML X)
	- USERAGENT

7. SSI (php 함수 및 환경변수 수집해서 넣기)
	- DATA

8. BOF 필터 X
9. 정보노출 필터 X
'''
def check_atktype(filename):
	filename = filename.lower()

	if "cf" in filename:
		atk_type = 1

	elif "xs" in filename or "xss" in filename:
		atk_type = 2

	elif "sql" in filename or "si" in filename:
		atk_type = 3

	elif "pt" in filename or "uaa" in filename or "fup" in filename or "fu" in filename:
		atk_type = 4

	elif "oc" in filename:
		atk_type = 5

	elif "au" in filename:
		atk_type = 6

	elif "ss" in filename:
		atk_type = 7

	elif "bo" in filename:
		atk_type = 8

	elif "il" in filename:
		atk_type = 9

	return atk_type

#리스트 원소의 길이를 구하는 함수  반환값은 리스트
#["aa","ccc","dddd"] 를 [2,3,4]이렇게 바꿔줌
def List2length(filter_list):
	list_length =[]

	for i in filter_list:
		list_length.append(len(i))
	return list_length


def debug_method(name,token,method):
	f = open("./error/"+name,"a",encoding="utf-8")
	f.write("\n"+method+" "+token+"\n++++++++++++++++++") #POST /test.asp 로 만들기 
	f.close()

def parseMultiPart(tokens,payload,count = 1):
	postbody={}
	data_body_list=[]
	data_body_length=[]
	data_body_type=[]

	boundary=''
	postbody["DATA"] = []
	postbody["DATA_MUTITYPE_LENGTH"] = []
	postbody["DATA_MUTITYPE_CONTENT-TYPE"] = []
		#print(tokens.index("boundary"))
	#print(tokens)
	if 'multipart/form-data;' in payload["CONTENT-TYPE"]:
		boundary = "--" + payload["CONTENT-TYPE"].split("boundary=")[1].split("\n")[0]
		


	elif "boundary=" in tokens:	
		boundary = "--"+tokens.split("boundary=")[1].split("\n")[0]
					
		
	else:
		for_search = tokens.split("\n")
		for token in for_search:
			if "content-disposition:" in token:
				prev_line = for_search[ for_search.index(token) - 1] 
				if "--" in prev_line:
					boundary = for_search[ for_search.index(token) - 1]
					break
				else:
					boundary = ''
		

	#POST가 아니라고 판단되면 그냥 빈값을 리턴
	if boundary == '' :	
		return postbody

	areas =  tokens.split(boundary) #boundary 나눌때 -- 더붙여서 이렇게 짬

	
	type_line =''
	index_type = 0
	disposition_line = ''
	index_disposition = 0
	FileName = []

	for area in areas[1:]: #boundary 시작부부터 끝까지
		area = area.lower( )#전부다소문자로


		if "content-type:" in area: # "content-type: "이 아니다 공백없애줘야함 왜냐면 line파싱할떄 replace로 공백없애주었기떄문

			#Content-Disposition: form-data; name="EWS_MESSAGE" 이런 한줄 Content-disposition: text/xml 이렇게 한줄이 될수도있다. 또는 content-type과 content-disposition이 두줄에 걸쳐 있을수있다.
			#index=area.index("\n\n")
			#원래는 위의 줄처럼 index를 구하나 newline다 없어진 로그 떄문에 content-type 바로 다음줄을 index_disposition 로 잡았음
			type_line = area.split("content-type:")[1].split("\n")[0]
			index_type = area.index(type_line)

			if "content-disposition" in area:
				disposition_line = area.split("content-disposition:")[1].split("\n")[0] 
				index_disposition = area.index(disposition_line)

			#if count == 493:
				#print(disposition_line.split('filename="')[1].split("\n")[0].split('"')[0])
			if 'filename="' in disposition_line:
				FileName = disposition_line.split('filename="')[1].split("\n")[0].split('"')[0]
				FileName = URL_word(FileName)
							
			if "content-disposition" not in area[index_type:]:  #content-type 다음줄에 content-type이 없으면 바로 다음줄이 데이터니까 +1
				final_index = index_type+len(type_line)+1       

			elif "content-disposition" in type_line: #content type 이 먼저나오고 뒤에 content disposition나오는데 그게  한줄로 있을때
				final_index = index_type+len(type_line)+1       

			else:                                   
				#content-type 다음줄에 content-disposition 이 있으면 다음 다음줄이 데이터니까 content-disposition잇는줄의 길이만큼 더해주고 나서 +1해준다
				#ontent-type잇는줄의 길이 = len("Content-Type:")+len(type_line)
				final_index = index_type+len(type_line)+len("content-disposition:")+len(disposition_line)+1


			content_type_multipart = type_line
			if( "text/" in content_type_multipart or "form-data" in content_type_multipart or "application/" in content_type_multipart\
					or "image/jpeg" in content_type_multipart):    #파일형식은 제외

				#content_type_mutipart랑 똑같지만 payload dictionary에 넣는용도
				data_body_type.append(type_line.split(";")[0])  # ; 을 고려해주었음

				#base64로 만들기
				data_body_str = area[final_index:]
				data_body_str = data_body_str.replace("\n"," ") #이전 작업에서 패킷에 뉴라인을 일일히 다해주었기떄문에 다시 뉴라인을 " "으로 replace해서 데이터를 한줄로 만들어줌 

				data_body_urldecode = urllib.parse.unquote(data_body_str)
				data_body_base64 = base64.b64encode(data_body_urldecode.encode("utf-8")).decode("utf-8")
				data_body_list.append(data_body_base64) #data_body 다 가져오기
				
				data_body_length.append(len(area[final_index:]))    #Content-type: form-data; name="EWS_MESSAGE" 이런거에서 길이만큼 더해주고 \n을 +1해줘서 다음줄 index를 가르키게함

		elif "content-disposition:" in area:    #content-type파싱과 똑같은 동작수행

			#Content-Disposition: form-data; name="EWS_MESSAGE" 이런 한줄 Content-disposition: text/xml 이렇게 한줄이 될수도있다. 또는 content-type과 content-disposition이 두줄에 걸쳐 있을수있다.
			#index=area.index("\n\n")
			#원래는 위의 줄처럼 index를 구하나 newline다 없어진 로그 떄문에 content-type 바로 다음줄을 index_disposition 로 잡았음
			
			disposition_line = area.split("content-disposition:")[1].split("\n")[0] 
			index_disposition = area.index(disposition_line)

			if "content-type" in area:
				type_line = area.split("content-type:")[1].split("\n")[0]
				index_type = area.index(type_line)

			if 'filename="' in disposition_line:
				FileName = disposition_line.split('filename="')[1].split("\n")[0].split('"')[0]
				FileName = URL_word(FileName)

			if "content-type" not in area[index_disposition:]:  #content-diposition 다음줄에 content-type이 없으면 바로 다음줄이 데이터니까 +1
				final_index = index_disposition+len(disposition_line)+1

			elif "content-type" in disposition_line:    # content disposition이 먼저나오고 뒤에 content-type이 따라나오는데 그게 한줄로 있을때
				final_index = index_disposition+len(disposition_line)+1

			else:                                   
				#content-diposition 다음줄에 content-type이 있으면 다음 다음줄이 데이터니까 content-type잇는줄의 길이만큼 더해주고 나서 +1해준다
				#ontent-type잇는줄의 길이 = len("Content-Type:")+len(type_line)
				final_index = index_disposition+len(disposition_line)+len("Content-Type:")+len(type_line)+1

			#for debugging
			#if count == 1583:
				#print(area[final_index:])

			content_disposition_multipart = disposition_line
			if( "text/" in content_disposition_multipart or "form-data" in content_disposition_multipart):  #파일형식은 제외

				#content_disposition_mutipart랑 똑같지만 payload dictionary에 넣는용도
				data_body_type.append(disposition_line.split(";")[0])   # ; 을 고려해주었음

				#base64로 만들기
				data_body_str = area[final_index:]
				data_body_str = data_body_str.replace("\n"," ") #이전 작업에서 패킷에 뉴라인을 일일히 다해주었기떄문에 다시 뉴라인을 " "으로 replace해서 데이터를 한줄로 만들어줌 

				data_body_urldecode = urllib.parse.unquote(data_body_str)
				data_body_base64 = base64.b64encode(data_body_urldecode.encode("utf-8")).decode("utf-8")
				data_body_list.append(data_body_base64) #data_body 다 가져오기
				
				data_body_length.append(len(area[final_index:]))    #Content-Disposition: form-data; name="EWS_MESSAGE" 이런거에서 길이만큼 더해주고 \n을 +1해줘서 다음줄 index를 가르키게함



	postbody["DATA"] = data_body_list + payload["DATA"] + encode_list(FileName)
	postbody["DATA_MUTITYPE_LENGTH"] = data_body_length         
	postbody["DATA_MUTITYPE_CONTENT-TYPE"] = data_body_type

	#if count == 1992:
		#print(boundary)
		#print(decode_base64(postbody["DATA"]))	
	return postbody				


#1037 1583(유형2) , 1538(유형25) 보기
def parsePOST(tokens,payload,count=1):	#token 사용할떄 꼭 lower해줘야함!!!
	type = payload["CONTENT-TYPE"].lower()
	tokens = tokens.lower()

	length = payload["CONTENT-LENGTH"]	#POST에 데이터가잇는경우는 contentlength가 있어야하고 0보다커야함
	if length =='': length = 0			#contentlength가 헤더에 애초에 없을경우 0으로 설정
	else: length = int(length)			#contentlength를 int형으로 변환

	postbody={}							#payload딕셔너리에 추가시키기위한 , 딕셔너리 반환값인 , postbody
	#여기는 lower()로 소문자가 되어잇어서 GET이 아니라 get이다! 디버깅할떄 주의 
	if "application/x-www-form-urlencoded" in type and length>0:
		body = tokens.split("\n")
		try: 
			index = tokens.index("\n\n")#http body 시작부분 찾기
			data_body = tokens[index+2:index+2+length] # [http body 시작 : http body 끝]
			data_body_list = parseparam(data_body)
			postbody["DATA"] = data_body_list + payload["DATA"]
		except:
			#print(tokens.replace("\n"," "))
			full_packet_urldecode = urllib.parse.unquote(tokens.replace("\n"," "))
			full_packet_base64 = base64.b64encode(full_packet_urldecode.encode("utf-8")).decode("utf-8")
			postbody["DATA"] = [full_packet_base64]
			debug_method("POST_urlencode.txt",tokens,"POST")
			pass 
		postbody["DATA_MUTITYPE_LENGTH"] = ""
		postbody["DATA_MUTITYPE_CONTENT-TYPE"] = ""
	
	#여기를 content-dispostion일떄 로 분기하기 
	elif 'content-disposition:' in tokens and length>0:
		
		try:
			postbody.update(parseMultiPart(tokens,payload,count))
			#postbody["DATA"] = data_body_list + payload["DATA"]
			#postbody["DATA_MUTITYPE_LENGTH"] = data_body_length         
			#postbody["DATA_MUTITYPE_CONTENT-TYPE"] = data_body_type
		except: 
			debug_method("multipart.txt",tokens,"POST")
			pass

	return postbody


'''
파싱 주요 함수
'''
# 1-1 유형은 URL 과 URL ?뒤에 따라오는 DATA를 뽑을수있음 즉,
# 1 유형 추출가능 KEY : URL , DATA
def filter_parse_type_11(line,atk_type,count=1):
	uri = []
	data = []
	filter_list = []

	line.replace(" ","%20")
	tokens = line.upper().split('\n')
	tokens2 = tokens[0].split("?")

	#URI 넣기
	uri = tokens2[0] 
	uri = URL_word(uri)

	#/section/kwdList.php?kwd=??N?????a??O?1111111 
	#위와 같은경우도 파싱하기위해서 tokens[1:]로 첫번째 ?뒤에것들 다가져온다음에 합치기를하였음
	params = ''.join(tokens2[1:]) 
	data = parseparam(params.replace("&amp;","&"),count)

	'''
	공격유형별로 필요한부분만 뽑기
	'''
	if atk_type==1 or atk_type==2:
		filter_list += decode_base64(data)
		filter_list += uri


	elif atk_type==3 or atk_type==5 or atk_type==7:
		filter_list += decode_base64(data)

	elif atk_type==4:
		filter_list += decode_base64(data)
		filter_list += uri

	elif atk_type == 8 or 9:	#BOF 와 정보누출(IL)은 파싱안하기로햇으므로 그냥 line그대로 리턴해줌
		filter_list = line 

	return filter_list



# 1-2 유형은 정상패킷이나 앞에 GET이나 POST같은 메소드 명만 없는경우
# 1-2 유형 추출가능 KEY : URL , DATA , COOKIE , REFERER , USER-AGENT
def filter_parse_type_12(line,atk_type,count=1):

	filter_list = []

	uri = []
	data = []
	cookie =[]
	referer = []
	useragent = ""

	line = "POST\n"+line #임의로 만들어준다 유형2와 호환용
	tokens = line.upper().split('\n')
	tokens2 = tokens[1].split("?")

	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":'',\
				"DATA_MUTITYPE_LENGTH":[], "DATA_MUTITYPE_CONTENT-TYPE":[]}

	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		payload.update(payload_add("REFERER:",token))
		payload.update(payload_add("USER-AGENT:",token))

		if payload["CONTENT-TYPE"] == '':	#multipart 파싱할때 content-type을 multipart의 content type으로 덮어쓰는경우를 방지. FU(Train.csv) 1037라인 같은곳에서 파싱이 잘안됨
			payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))


	if len(tokens2)>1:
		params = ''.join(tokens2[1:]) 
		payload["DATA"] = parseparam(params.replace("&AMP;","&"),count)

	payload.update(parsePOST(line.lower() , payload,count))

	data += payload["DATA"]
	
	#a=decode_base64(data)
	#for i in a:
		#if i == 'connection:close':
			#print(count)
			#print(a)	

	#uri 에 바로 /formdata들어가는거짜기
	if not ("form-data" in tokens[1].lower() and "boundary=" in tokens[1].lower()) :
		uri = tokens2[0]	#URI
		uri = URL_word(uri)	

	#if count == 1721:
		#print(uri)
	'''
	공격유형별로 필요한부분만 뽑기
	'''

	#DATA, URL COOKIE
	if atk_type ==1 or atk_type==2:	
		cookie = payload["COOKIE"]

		filter_list += decode_base64(data)
		filter_list += uri
		filter_list += cookie

	#DATA,REFERER
	elif atk_type == 3: 			

		referer = payload["REFERER"]

		if len(referer)>0:
			tokens3 = referer.split("?")				
			referer = tokens3[0]
			referer = URL_word(referer)	
			referer = encode_list(referer)	
			data_referer = []

			if len(tokens3) > 1:	
				params = ''.join(tokens3[1:]) 		
				data_referer = parseparam(params.replace("&AMP;","&"),count)
			else:
				temp = tokens3[0].split('/')[-1]
				temp = URL_word(temp)
				temp = encode_list(temp)
				if len(temp) > 0:
					#data.append(base64.b64encode(temp).decode("utf-8"))
					data_referer += temp	

			if len(data) > 0:
				data += data_referer
			else:
				data += data_referer

		filter_list += data
		filter_list += referer
		#data , referer가 base64 인코딩 되어있는것이어서 filter_list에 decode_base64함수를 적용하였음
		filter_list = decode_base64(filter_list)	

		filter_list += payload["COOKIE"]


	#URL , DATA
	elif atk_type == 4: 			
		filter_list += uri
		filter_list += decode_base64(data)

	

	#DATA
	elif atk_type == 5 or atk_type==7:	
		filter_list += decode_base64(data)

	#USERAGENT
	elif atk_type == 6: 			
		useragent = payload["USER-AGENT"]
		filter_list.append(useragent)

	elif atk_type == 8 or 9:	#BOF 와 정보누출(IL)은 파싱안하기로햇으므로 그냥 line그대로 리턴해줌
		filter_list.append(line)


	return filter_list

def filter_parse_type_2(line,atk_type,count=1):

	filter_list = []

	uri = []
	data = []
	cookie =[]
	referer = []
	useragent = ""

	tokens = line.upper().split('\n')
	tokens2 = tokens[1].split("?")

	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":'',\
				"DATA_MUTITYPE_LENGTH":[], "DATA_MUTITYPE_CONTENT-TYPE":[]}

	payload["METHOD"] = line[:10]
	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		payload.update(payload_add("REFERER:",token))
		payload.update(payload_add("USER-AGENT:",token))

		if payload["CONTENT-TYPE"] == '':	#multipart 파싱할때 content-type을 multipart의 content type으로 덮어쓰는경우를 방지. FU(Train.csv) 1037라인 같은곳에서 파싱이 잘안됨
			payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))

	if len(tokens2)>1:
		params = ''.join(tokens2[1:]) 
		payload["DATA"] += parseparam(params.replace("&AMP;","&"),count)



	if "POST".lower() in payload["METHOD"].lower() or "HTTP/1.1".lower() in line[:14].lower() or "HTTP/1.0" in line[:14].lower():	#POST인지 체크
		payload.update(parsePOST(line.lower() , payload,count))

	data += payload["DATA"]


	#uri 에 바로 /formdata들어가는거짜기
	if "HTTP/1.1".lower() not in payload["METHOD"].lower():
		uri = tokens2[0]	#URI
		uri = URL_word(uri)	

	#if count ==1992:
		#print(line[:10])
		#print(uri)
	'''
	공격유형별로 필요한부분만 뽑기
	'''

	#DATA, URL COOKIE
	if atk_type ==1 or atk_type==2:	
		cookie = payload["COOKIE"]


		#print(data)
		filter_list += decode_base64(data)
		filter_list += uri
		filter_list += cookie

	#DATA,REFERER
	elif atk_type == 3: 			

		referer = payload["REFERER"]

		if len(referer)>0:
			tokens3 = referer.split("?")				
			referer = tokens3[0]
			referer = URL_word(referer)	
			referer = encode_list(referer)	
			data_referer = []

			if len(tokens3) > 1:	
				params = ''.join(tokens3[1:]) 		
				data_referer = parseparam(params.replace("&AMP;","&"),count)
			else:
				temp = tokens3[0].split('/')[-1]
				temp = URL_word(temp)
				temp = encode_list(temp)
				if len(temp) > 0:
					#data.append(base64.b64encode(temp).decode("utf-8"))
					data_referer += temp	

			if len(data) > 0:
				data += data_referer
			else:
				data += data_referer

		filter_list += data
		filter_list += referer
		#data , referer가 base64 인코딩 되어있는것이어서 filter_list에 decode_base64함수를 적용하였음
		filter_list = decode_base64(filter_list)	

		filter_list +=payload["COOKIE"]


	#URL , DATA
	elif atk_type == 4: 			
		filter_list += uri
		filter_list += decode_base64(data)
	

	#DATA
	elif atk_type == 5 or atk_type==7:	
		filter_list += decode_base64(data)

	#USERAGENT
	elif atk_type == 6: 			
		useragent = payload["USER-AGENT"]
		filter_list.append(useragent)

	elif atk_type == 8 or 9:	#BOF 와 정보누출(IL)은 파싱안하기로햇으므로 그냥 line그대로 리턴해줌
		filter_list.append(line)


	return filter_list

#3-1 데이터만 붙어있을경우
def filter_parse_type_31(line,atk_type,count = 1):



	filter_list=[]
	data =[]

	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":'',\
				"DATA_MUTITYPE_LENGTH":[], "DATA_MUTITYPE_CONTENT-TYPE":[]}
	
	payload.update( parseMultiPart(line,payload,count)	)

	if payload["DATA"] !=[] :
		data += payload["DATA"]
		#print(decode_base64(data))
		#print(count)

	elif "{" in line[:2]:
		data += parsejson(line)

	# A=abcd&B=sdfdf 꼴일때
	# A=ddagdg 같이 &없이 변수 하나인것도  파싱함 
	else:
		data += parseparam(line,count) 


	'''
	공격유형별로 필요한부분만 뽑기
	'''
	#DATA
	if atk_type==1 or atk_type==2 or atk_type==3 or atk_type==5 or atk_type==7 or atk_type == 4:
		#filter_list = list(set(parseparam(line)))	#중복제거
		filter_list = data

		#decode_base64(filter_list)해준이유는 parseparam함수가 base64인코딩한 리스트를 반환하기떄문
		#다른 함수는 filter_parse_typeN 에서 data리스트에 decode_base64()를 사용해서 디코드를 한후에 filter_list에 값을 넣어주었음
		filter_list = decode_base64(filter_list)

	elif atk_type == 8 or atk_type == 9:	#BOF 와 정보누출(IL)은 파싱안하기로햇으므로 그냥 line그대로 리턴해줌
		filter_list.append(line)

	return filter_list

#3유형은 2유형에서 중간에 잘린 데이터를 처리하는 유형, 그래서 parseparam()부분과 URI가져오는 부분이 없다.
def filter_parse_type_32(line,atk_type,count = 1):

	filter_list = []

	uri = []
	data = []
	cookie =[]
	referer = []
	useragent = ""

	tokens = line.upper().split('\n')
	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":'',\
				"DATA_MUTITYPE_LENGTH":[], "DATA_MUTITYPE_CONTENT-TYPE":[]}
	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		payload.update(payload_add("REFERER:",token))
		payload.update(payload_add("USER-AGENT:",token))
		payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))

	payload.update( parseMultiPart(line,payload,count)	)
	data += payload["DATA"]


	'''
	공격유형별로 필요한부분만 뽑기
	'''
	#DATA, COOKIE
	if atk_type ==1 or atk_type==2:	
		cookie = payload["COOKIE"]

		filter_list += decode_base64(data)
		filter_list += cookie

	#DATA,REFERER
	elif atk_type == 3: 			

		referer = payload["REFERER"]	
		if len(referer)>0:
			tokens3 = referer.split("?")	

			referer = tokens3[0]
			referer = URL_word(referer)	
			referer = encode_list(referer)	
			data_referer = []

			if len(tokens3) > 1:			
				params = ''.join(tokens3[1:]) 		
				data_referer = parseparam(params.replace("&AMP;","&"),count)
			else:
				temp = tokens3[0].split('/')[-1]
				temp = URL_word(temp)
				temp = encode_list(temp)
				if len(temp) > 0:
					#data.append(base64.b64encode(temp).decode("utf-8"))
					data_referer += temp	

			if len(data) > 0:
				data += data_referer
			else:
				data = data_referer

		filter_list += data
		filter_list += referer
		#data , referer가 base64 인코딩 되어있는것이어서 filter_list에 decode_base64함수를 적용하였음
		filter_list = decode_base64(filter_list)	

		filter_list += payload["COOKIE"]


	#URL , DATA
	#유형3은 URL가져오는 부분이 없어서 그냥 공백처리
	elif atk_type == 4: 			

		filter_list = []
		filter_list += decode_base64(data)

	
	#DATA
	elif atk_type == 5 or atk_type==7:	
		filter_list += decode_base64(data)

	#USERAGENT
	elif atk_type == 6: 			
		useragent = payload["USER-AGENT"]
		filter_list.append(useragent)

	#no parsing
	elif atk_type == 8 or 9:	#BOF 와 정보누출(IL)은 파싱안하기로햇으므로 그냥 line그대로 리턴해줌
		filter_list.append(line)


	return filter_list

def filter(line , atk_type,count=1):


	line_origin = copy.deepcopy(line)
	line_origin = line_origin.strip()

	line = line.strip()
	line = line.replace('#015#012','\n')
	line = line.replace(': ', ':')
	line = line.replace('; ', ';')
	line = line.replace(', ', ',')
	line = line.replace(" ", '\n')

	data_type = -1
	data_type = check_DataType(line,count)

	#print("---------------"+str(count)+"------------------	DataType : "+str(data_type)+"\n"+line+"\n\n")

	line = line.lower()

	# "/*&" ---> "/*" 로 변환 
	line = line.replace("%2f%2a&","%2f%2a")	

	filter_list = []

	#데이터가 아무것도 없으면
	if data_type == -1:
		filter_list = []

	#유형 1이면 
	if data_type == 11:
		filter_list = filter_parse_type_11(line_origin,atk_type,count)

	if data_type == 12:
		filter_list = filter_parse_type_12(line,atk_type,count)

	#유형 2이면
	if data_type == 2:
		filter_list = filter_parse_type_2(line,atk_type,count)

	elif data_type ==31:
		filter_list = filter_parse_type_31(line,atk_type,count)	

	elif data_type == 32:
		filter_list = filter_parse_type_32(line,atk_type,count)


	#filter_list에 공백 들어가는거 삭제
	filterlist_for_search = filter_list[:]	#탐색용 배열 
	for i in filterlist_for_search:
		if i =="":
			filter_list.remove("")\
	

	#for i in filter_list:
		#if i == 'form-data;boundary=----webkitformboundarysyaasogjpo89jr63':
			#print(count)
			#print(data_type)
			#print(line)
			#print(filter_list)


	filter_list = [item.lower() for item in filter_list]
	filter_list = list(set(filter_list))

	#중복제거를 하고싶으시면 주석을 제거해주세요 
	#중복제거
	#filter_list = list(set(filter_list))

	#to lowercase
	#filter_list = [item.lower() for item in filter_list]

	#정렬
	#filter_list.sort()

	#word만뽑고싶으시면 주석을 제거하시면 됩니다.
	#word만 뽑기
	#filter_list = Word_only(filter_list)

	#길이만 뽑고싶으시면 주석을 제거해주세요
	#길이만 뽑기
	#filter_list_len = List2length(filter_list)

	#for debugging
	#return ["datatype: "+str(data_type)]+filter_list

	return filter_list
		



