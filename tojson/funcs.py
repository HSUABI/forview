import os
import csv
import json
import urllib.parse
import base64


'''	자질구레한 함수들
	이건 안봐도 됩니다'''

#페이로드 몇번째 열에 있는지 찾는 코드
def index_dict(string,dirname):
	filenames = search(dirname)	#file search
	try: filenames.remove("desktop.ini")	#desktop.ini 잇으면 삭제 없으면 패스
	except: pass
	indices={}
	for file in filenames: #파일 하나씩 열기
		f = open(dirname+file ,'r',encoding='utf-8')
		rdr = csv.reader(f)
		for line in rdr: # 첫행 읽기
			row_1 = line
			break
		indices[file] = find_index(row_1,string)	# 페이로드 열이 몇번째 열에 잇는지 dictionary에 저장
		if indices[file] == 99:						# "정오탐" ,"결과" 이 열 예외처리용 
			del(indices[file])

		f.close()
	return indices

#특정 열만 추출해서 export폴더에 생성
def extract_col(index_dict):
	filenames = search("./logs/") #file search
	filenames.remove("desktop.ini")
	for file in filenames:
		f = open("./logs/"+file ,'r',encoding='utf-8')
		f2 = open("./export/"+file, 'wt' ,encoding='utf-8',newline='')
		rdr = csv.reader(f)
		wr = csv.writer(f2)
		index = index_dict[file]
		for line in rdr:
			paylod=[]
			paylod.append(line[index])
			wr.writerow(paylod)
		f.close()
		f2.close()

def search(dirname):
    filenames = os.listdir(dirname)
    return filenames

def find_index(row_1,string):
	cnt = 0
	for i in row_1:
		if string in i:
			break
		cnt=cnt+1
	if len(row_1) == cnt:
		return 99
	return cnt
def debug_method(name,token,method):
	f = open("./error/"+name,"a",encoding="utf-8")
	f.write("\n"+method+" "+token+"\n++++++++++++++++++") #POST /test.asp 로 만들기 
	f.close()

def debug(name,line):
	f = open("./error/"+name,"a",encoding="utf-8")
	f.write("\n"+line+"\n++++++++++++++++++") #POST /test.asp 로 만들기 
	f.close()

def totxt(token,method,file):
	f2 = open(method+'.txt','a',encoding="utf-8")			
	#f2 = open("HTTP response"+'.txt','a',encoding="utf-8")	#HTTP response 추출용 코드
	f2.write("-------"+file+"-------\n")
	f2.write(method+" "+token)								
	#f2.write(method+token)	#HTTP response 추출용 코드
	f2.write("\n------end--------\n\n")
	f2.close()




'''	파싱에 본격적으로 사용되는 함수들
	이 부분부터 코드보시면 제가 어떻게 파싱하는지 압니다.'''
	
def strcat(token2): # 파라미터에 = 들어갔을경우 예외처리
	str_=''
	for i in token2[1:]:		
		if(i==token2[-1]):	#id=1%20and%201=2%20union 이럴때 "1=2" 넣기위함
			str_ +=i
		else:				# 맨마지막에 =붙이면안됨
			str_+= (i+"=")
	return str_

def parseparam(params):
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

def payload_add(string , token):	#URL , Host , UserAgent 등등이 인자로 들어감
	payload={}						#parePOST의 postbody와 같은 역할

	#request "Cookie : xxx" 와 response의 "Set-Cookie: JSESSIONID=jZ0b5v~~`"를 다 커버하는 코드임
	if string in token and string == "Cookie: ".lower():		 
		cookies = token.split(string)[1].split("\n")[0]
		cookie_list = parsecookie(cookies)
		payload[string.split(": ")[0].upper()] = cookie_list

	elif(string in token):
		# "Host: " --> "HOST"
		payload[string.split(": ")[0].upper()] = token.split(string)[1].split("\n")[0]

	else:
		payload[string.split(": ")[0].upper()] = '' 

	return payload
def parsePUT(token,payload):
	length = payload["CONTENT-LENGTH"]	#PUT에 데이터가잇는경우는 contentlength가 있어야하고 0보다커야함
	if length =='': length = 0			#contentlength가 헤더에 애초에 없을경우 0으로 설정
	else: length = int(length)			#contentlength를 int형으로 변환
	try:
		data_body_list=[]		
		index = token.index("\n\n")#http body 시작부분 찾기
		data_body = token[index+2:index+2+length] # [http body 시작 : http body 끝]
		data_body_urldecode = urllib.parse.unquote(data_body)
		data_body_base64 = base64.b64encode(data_body_urldecode.encode("utf-8")).decode("utf-8")
		data_body_list.append(data_body_base64)	#data_body 다 가져오기
		payload["DATA"] = data_body_list
	except:
		payload["DATA"] =[]
		debug_method("PUT.txt",token,"PUT")
	return payload

def parseRESPONSE(token,payload):
	type = payload["CONTENT-TYPE"]

	if "text/html" in type:
		try:
			data_body_list=[]
			index = token.index("\n\n")
			data_body = token[index+2:-1]	# contentlength가 없는데 body잇는경우가 많아서 length 안넣어줌	
			data_body_urldecode = urllib.parse.unquote(data_body)
			data_body_base64 = base64.b64encode(data_body_urldecode.encode("utf-8")).decode("utf-8")
			data_body_list.append(data_body_base64)
			payload["DATA"] = data_body_list
		except:
			payload["DATA"] =[]
			debug_method("RESPONSE.txt",token,"HTTP/1.1")

	if "application/json" in type:
		try:
			data_body_list=[]
			index = token.index("\n\n")
			data_body = token[index+2:-1]	# contentlength가 없는데 body잇는경우가 많아서 length 안넣어줌	
			data_body_list = parsejson(data_body)
			payload["DATA"] = data_body_list
		except:
			payload["DATA"] = []
			debug_method("RESPONSE_JSON.txt",token,"HTTP/1.1")

	return payload

def parsePOST(token,payload):

	type = payload["CONTENT-TYPE"]
	length = payload["CONTENT-LENGTH"]	#POST에 데이터가잇는경우는 contentlength가 있어야하고 0보다커야함
	if length =='': length = 0			#contentlength가 헤더에 애초에 없을경우 0으로 설정
	else: length = int(length)			#contentlength를 int형으로 변환

	postbody={}							#payload딕셔너리에 추가시키기위한 , 딕셔너리 반환값인 , postbody
	#여기는 lower()로 소문자가 되어잇어서 GET이 아니라 get이다! 디버깅할떄 주의 
	if "application/x-www-form-urlencoded" in type and length>0:
		body = token.split("\n")
		try: 
			index = token.index("\n\n")#http body 시작부분 찾기
			data_body = token[index+2:index+2+length] # [http body 시작 : http body 끝]
			data_body_list = parseparam(data_body)
			postbody["DATA"] = data_body_list
		except:
			debug_method("POST_urlencode.txt",token,"POST")
			pass 
		postbody["DATA_MUTITYPE_LENGTH"] = ""
		postbody["DATA_MUTITYPE_CONTENT-TYPE"] = ""

	elif 'multipart/form-data;' in type and length>0:
		try: 
			data_body_list=[]
			data_body_length=[]
			data_body_type=[]
			boundary = payload["CONTENT-TYPE"].split("boundary=")[1].split("\n")[0]
			areas =  token.split("--"+boundary) #boundary 나눌때 -- 더붙여서 이렇게 짬
			for area in areas[1:]: #boundary 시작부부터 끝까지
				area = area.lower( )#전부다소문자로
				if "content-type: " in area:
					index=area.index("\n\n")

					#multipart에 잇는 contenttype가져오기
					content_type_multipart = area.split("content-type: ")[1].split("\n")[0]
					if( "text/" in content_type_multipart or "form-data" in content_type_multipart):	#파일형식은 제외

						#content_type_mutipart랑 똑같지만 payload dictionary에 넣는용도
						data_body_type.append(area.split("content-type: ")[1].split("\n")[0])

						#base64로 만들기
						data_body_str = area[index+2:]
						data_body_urldecode = urllib.parse.unquote(data_body_str)
						data_body_base64 = base64.b64encode(data_body_urldecode.encode("utf-8")).decode("utf-8")
						data_body_list.append(data_body_base64)	#data_body 다 가져오기
						
						data_body_length.append(len(area[index+2:]))

			postbody["DATA"] = data_body_list
			postbody["DATA_MUTITYPE_LENGTH"] = data_body_length			
			postbody["DATA_MUTITYPE_CONTENT-TYPE"] = data_body_type
		except: 
			debug_method("multipart.txt",token,"POST")
			pass

	else:
		postbody["DATA_MUTITYPE_LENGTH"] = ""
		postbody["DATA_MUTITYPE_CONTENT-TYPE"] = ""
	return postbody

def tojson_oneline(line): #2019 logadmin csv파일 raw_data랑 request파싱
	payload={}
	#f = open("./error/logadmin2019.txt","a",encoding="utf-8")

	try:
		token = line.split(" /")[1]
	except:	#에러로그남기는게 시간 너무오래걸려서 한번 에러뽑고 이제 주석처리함
		#f.write(line+"\n")
		#f.write("\n+++++++++++++++++++\n")
		return 0			#" /"로 안나눠지면 패킷이 중간에 짤린거다 그래서 return 0해주고 예외처리
		pass
	payload["URL"] = "/"+token.split(" ")[0].split("?")[0]
	params = token.split(" ")[0].split("?")
	if len(params)==2:
		data = parseparam(params[1])
		payload["DATA"] = data
	else:
		payload["DATA"] = []
	if "POST" in line:
		payload["METHOD"] = "POST"
	elif "GET" in line:
		payload["METHOD"] = "GET"
	else:
		payload["METHOD"] = ""
	payload_str=json.dumps(payload, ensure_ascii=False, indent=4)

	#f.close()
	return payload_str

#input은 리스트	
#data리스트에서 영어 단어만찾아서 뽑고 그것을 data_only_word에넣는다.
#예시) data=["123124abc2423ggg434","qweop2139c--34dde"] ==>data_only_word-["abc","ggg","qweop","c","dde"]
#string:"123124abc2423ggg434" ,character는 string에서 문자 하나하나 , word:"abc" 
def DATA_word(data):
	data_only_word=[]
	word=""
	for string in data:
		string = base64.b64decode(string).decode("utf-8")	#base64풀어주기
		for character in string:
			if character.isalpha() == True:
				word += character
			elif character.isalpha() == False:
				data_only_word.append(word)
				word = ""

	#DATA에 공백 들어가는거 색제
	DATA_for_search = data_only_word[:]	#탐색용 배열 
	for i in DATA_for_search:
		if i =="":
			data_only_word.remove("")
	return data_only_word

def tojson(line,method,file):
	
	#response인지 request인지에따라 파싱이 살짝 다름
	if method == "HTTP/1.1 ":
		tokens = line.split("HTTP/1.1 ")	#HTTP response 추출용 코드
	else:
		tokens = line.split(method+" ")	#한 엑셀 행에 HTTP 패킷이 2개있는경우가 있어서 GET,POST으로 split함

	del(tokens[0])					 	#GET,POST으로 split했으니 맨앞은 아무거도없거나 필요없는값
	payload_str=''
	for token in tokens:
		payload = {}
		#totxt(token,method,file)	#txt로 뽑는거

		#url에서 ?뒤에오는 데이터들 dictionary에 추가
		params=token.split(" ")[0].split("?")	#?뒤의 파라미터들 가져오기
		if len(params)==2:						#파라미터가 존재를 하면
			data = parseparam( params[1].replace("&amp;","&") )	
			payload["DATA"] = data
		else:
			payload["DATA"] = []
		
		#http header부분 dictionary에 추가
		
		if method == "HTTP/1.1 ":	# HTTP Response 부분 파싱
			payload["METHOD"] = token.split(" ")[0]	# 200 , 404 , 503 이런것들 가져옴
			payload["URL"] = []
		else:
			payload["METHOD"] = method				#method
			payload["URL"] = token.split(" ")[0].split("?")[0]	#URL
		
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌	
		payload.update(payload_add("Referer: ".lower(),token.lower()))  	
		payload.update(payload_add("User-Agent: ".lower(),token.lower()))
		payload.update(payload_add("Content-Type: ".lower(),token.lower()))
		payload.update(payload_add("Host: ".lower(),token.lower()) ) 
		payload.update(payload_add("Content-Length: ".lower(),token.lower()))
		payload.update(payload_add("Connection: ".lower(),token.lower()))
		payload.update(payload_add("Cookie: ".lower(),token.lower()))

		#http body부분 dictionary에 추가
		if method == "POST":	#POST인지 체크
			payload.update(parsePOST(token.lower() , payload))
		else:
			payload["DATA_MUTITYPE_LENGTH"] = []
			payload["DATA_MUTITYPE_CONTENT-TYPE"] = []

		if method =="PUT":
			payload.update(parsePUT(token.lower(), payload))

		if method == "HTTP/1.1 ":
			payload.update( parseRESPONSE(token.lower(),payload) )

		#DATA에 공백 들어가는거 색제
		DATA_for_search = payload["DATA"][:]	#탐색용 배열 
		for i in DATA_for_search:
			if i =="":
				payload["DATA"].remove("")

		#패킷이 2~3개씩 한번에 있을경우 ,로 묶어줌 그래서 string으로 바꾸고 반환한다. 딕셔너리는 패킷한개 밖에 반환못한다.
		#{"NAME":"SONG"},{"NAME":"CAU"} 이렇게 ,로 JSON객체 묶음
		payload_str+=json.dumps(payload, ensure_ascii=False, indent=4)
		payload_str+="\n," 
	
	return payload_str

#사실상 main함수
def pay2json(line,file):		#엑셀 페이로드 열에서 한개의 셀 받음
	
	methods = ["GET","POST","HEAD","OPTIONS","PUT","DELETE","TRACE","CONNECT"]
	payload_json_bunch = '' #{"NAME":"SONG"},{"NAME":"CAU"} 이렇게 ,로 JSON객체 묶음

	for method in methods:
		if method+" /" in line:		# GET /naver.com/ 이런거
			payload_json_bunch += tojson(line,method,file)

	if "HTTP/1.1 " in line:
		payload_json_bunch += tojson(line,"HTTP/1.1 ",file)
	'''
	HTTP response 추출용 코드
	if "HTTP/1.1 " in line:
		payload_json_bunch += tojson(line,"HTTP/1.1 ",file)
	'''
	return payload_json_bunch[:-2]


#######################
#######################
#######################
'''
level1.kisa.XSS_total_shuffled파일 유형별로 나누어서 파싱 하는 함수
'''
#######################
#######################
#######################
#######################


def parse_type_3_1(line):

	payload={}
	data = line.replace("&amp;","&")
	payload["DATA"] = parseparam(data)
	return payload

def parse_type_3_2(line):

	payload = {}
	payoad["DATA"]=[]	#일단 비워둠 나중에 코드작성
	return payload

def tojson_3typeofdata(line):
	
	token = line
	payload = {}

	#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌	
	payload.update(payload_add("Referer: ".lower(),token.lower()))  	
	payload.update(payload_add("User-Agent: ".lower(),token.lower()))
	payload.update(payload_add("Content-Type: ".lower(),token.lower()))
	payload.update(payload_add("Host: ".lower(),token.lower()) ) 
	payload.update(payload_add("Content-Length: ".lower(),token.lower()))
	payload.update(payload_add("Connection: ".lower(),token.lower()))
	payload.update(payload_add("Cookie: ".lower(),token.lower()))

	chk = 0
	#Referer , User-Agent값들이 있었는지 조회 없으면 "" 이니까 chk=0이고 그런값들이잇으면 chk=1이됨
	for i in list(payload.values()):
		if i !="": 
			chk =1

	#Referer, HOST같은게 머 하나라도 없으면 data만잇는걸로 간주하고 유형 3-1로 파싱	
	if(chk==0):
		payload.update(parse_type_3_1(token))

	#Referer, HOST같은게 머 하나라도 들어가는게 있으면 그대로 하면됨,유형 3-2로 파싱
	elif(chk==1):
		a=1
		#3-2함수실행
		#payload.update(parse_type_3_2(token))

	#DATA에 공백 들어가는거 색제
	try:
		DATA_for_search = payload["DATA"][:]	#탐색용 배열 
		for i in DATA_for_search:
			if i =="":
				payload["DATA"].remove("")
	except:
		debug("3type.txt",line)


	return payload


#종민형 코드
def parse_type_1(line):

    payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":''}
    data = []

    tokens = line.split("?")
    payload["URI"] = tokens[0]	#URI
	
    if len(tokens) == 1:
	    temp = tokens[0].split('/')[-1].encode("utf-8")
	    if len(temp) > 0:
	        data.append(base64.b64encode(temp).decode("utf-8"))
    else:
	    temp = parseparam(tokens[1].replace("&amp;","&"))
	    if len(temp) > 1:
	        data = list(set(temp))
	    else:
	        data = temp
	
    payload["DATA"] = data
    return payload

def parse_type_2(line):

	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":''}
	tokens = line.upper().split('\n')

	payload["METHOD"] = tokens[0]
	tokens2 = tokens[1].split("?")
	payload["URI"] = tokens2[0]	#URI

	if len(tokens2) > 1:
		payload["DATA"] = parseparam(tokens2[1].replace("&AMP;","&"))

	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		payload.update(payload_add("REFERER:",token))
		#payload.update(payload_add("user-agent:",token.lower()))
		payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))

	if len(payload["REFERER"]) > 0:
		tokens3 = payload["REFERER"].split("?")
		payload["REFERER"] = tokens3[0]

		data = []
		if len(tokens3) > 1:			
			data = parseparam(tokens3[1])
		else:
			temp = tokens3[0].split('/')[-1].encode("utf-8")
			if len(temp) > 0:
				data.append(base64.b64encode(temp).decode("utf-8"))

		if len(payload["DATA"]) > 0:
			payload["DATA"] += data
		else:
			payload["DATA"] = data

	if len(payload["DATA"]) > 1:
		payload["DATA"] = list(set(payload["DATA"]))

	return payload

'''
유형1 	: 맨앞이 / 인 경우
유형2 	: 풀패킷이 다있는경우
유형3-1 : 데이터만 따딱 있는경우 (변수=갑&변수=값)
유형3-2 : 유형2에서 중간에 잘려있는거 COOKIE,HOST같은것들이 있으면 유형 3-2

'''
def tojson_single(line):
	line = line.strip()
	
	if line[0] == '/':
		return parse_type_1(line)

	line = line.replace('#015#012','\n')
	line = line.replace(': ', ':')
	line = line.replace('; ', ';')
	line = line.replace(', ', ',')
	line = line.replace(" ", '\n')

	if "GET" in line[:4] or "POST" in line[:4]:
		return parse_type_2(line)

	payload = {"DATA":[], "METHOD":'', "URI":'', "USER-AGENT":'', "REFERER":'', "COOKIE":[], "CONTENT-TYPE":'', "CONTENT-LENGTH":'', "CONNECTION":'', "HOST":''}
	if not "HTTP/1.1" in line:
		payload["DATA"] = list(set(parseparam(line)))
		return payload

	tokens = line.upper().split('\n')
	for token in tokens:
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌
		#payload.update(payload_add("user-agent:",token.lower()))
		payload.update(payload_add("REFERER:",token))		
		payload.update(payload_add("CONTENT-TYPE:",token))
		payload.update(payload_add("HOST:",token)) 
		payload.update(payload_add("CONTENT-LENGTH:",token))
		payload.update(payload_add("CONNECTION:",token))
		payload.update(payload_add("COOKIE:",token))

	if len(payload["REFERER"]) > 0:
		tokens3 = payload["REFERER"].split("?")
		payload["REFERER"] = tokens3[0]
		data = []
		if len(tokens3) > 1:			
			data = parseparam(tokens3[1])
		else:
			data.append(base64.b64encode(tokens3[0].split('/')[-1].encode("utf-8")).decode("utf-8"))

		if len(payload["DATA"]) > 0:
			payload["DATA"] += data
		else:
			payload["DATA"] = data

		if len(payload["DATA"]) > 1:
			payload["DATA"] = list(set(payload["DATA"]))

		return payload
	else:
		print("New3: ")
		print(line)

	return payload


#######################
#######################
#######################
#######################
#######################
'''AI 팀 연동용 코드 '''
#######################
#######################
#######################
#######################
#######################
def tojson_ai(line,method,file):
	
	#response인지 request인지에따라 파싱이 살짝 다름
	if method == "HTTP/1.1 ":
		tokens = line.split("HTTP/1.1 ")	#HTTP response 추출용 코드
	else:
		tokens = line.split(method+" ")	#한 엑셀 행에 HTTP 패킷이 2개있는경우가 있어서 GET,POST으로 split함

	del(tokens[0])					 	#GET,POST으로 split했으니 맨앞은 아무거도없거나 필요없는값
	payload_str=''
	for token in tokens:	# for문은 엑셀 한칸에 패킷여러번있을때를 고려해서 for문짠거입니다. 그래서 ai팀분들이 돌리실때는 무조건for문한번돌거에요.
		payload = {}
		#totxt(token,method,file)	#txt로 뽑는거

		#url에서 ?뒤에오는 데이터들 dictionary에 추가
		params=token.split(" ")[0].split("?")	#?뒤의 파라미터들 가져오기
		if len(params)==2:						#파라미터가 존재를 하면
			data = parseparam( params[1].replace("&amp;","&") )	
			payload["DATA"] = data
		else:
			payload["DATA"] = []
		
		#http header부분 dictionary에 추가
		
		if method == "HTTP/1.1 ":	# HTTP Response 부분 파싱
			payload["METHOD"] = token.split(" ")[0]	# 200 , 404 , 503 이런것들 가져옴
			payload["URL"] = []
		else:
			payload["METHOD"] = method				#method
			payload["URL"] = token.split(" ")[0].split("?")[0]	#URL
		
		#content-type , Content-Type 이런거 떄문에 token을 소문자로 바꾸어줌	
		payload.update(payload_add("Referer: ".lower(),token.lower()))  	
		payload.update(payload_add("User-Agent: ".lower(),token.lower()))
		payload.update(payload_add("Content-Type: ".lower(),token.lower()))
		payload.update(payload_add("Host: ".lower(),token.lower()) ) 
		payload.update(payload_add("Content-Length: ".lower(),token.lower()))
		payload.update(payload_add("Connection: ".lower(),token.lower()))
		payload.update(payload_add("Cookie: ".lower(),token.lower()))

		#http body부분 dictionary에 추가
		if method == "POST":	#POST인지 체크
			payload.update(parsePOST(token.lower() , payload))
		else:
			payload["DATA_MUTITYPE_LENGTH"] = []
			payload["DATA_MUTITYPE_CONTENT-TYPE"] = []

		if method =="PUT":
			payload.update(parsePUT(token.lower(), payload))

		if method == "HTTP/1.1 ":
			payload.update( parseRESPONSE(token.lower(),payload) )

		#DATA에 공백 들어가는거 색제
		DATA_for_search = payload["DATA"][:]	#탐색용 배열 
		for i in DATA_for_search:
			if i =="":
				payload["DATA"].remove("")

		#패킷이 2~3개씩 한번에 있을경우 ,로 묶어줌 그래서 string으로 바꾸고 반환한다. 딕셔너리는 패킷한개 밖에 반환못한다.
		#{"NAME":"SONG"},{"NAME":"CAU"} 이렇게 ,로 JSON객체 묶음
		#payload_str+=json.dumps(payload, ensure_ascii=False, indent=4)
		#payload_str+="\n," 
	
	return payload

#사실상 main함수
def pay2json_ai(line,file):		#payload string을 받음
	
	methods = ["GET","POST","HEAD","OPTIONS","PUT","DELETE","TRACE","CONNECT"]
	payload_json_bunch = '' 

	for method in methods:
		if method+" /" in line:		# GET /naver.com/ 이런거
			return tojson_ai(line,method,file)	#ai팀 용 코드는 한개의 payload에 대해 파싱하고 dict를 반환 

	if "HTTP/1.1 " in line:
		return tojson_ai(line,"HTTP/1.1 ",file) #ai팀 용 코드는 한개의 payload에 대해 파싱하고 dict를 반환
	'''
	HTTP response 추출용 코드
	if "HTTP/1.1 " in line:
		payload_json_bunch += tojson(line,"HTTP/1.1 ",file)
	'''
	return false
