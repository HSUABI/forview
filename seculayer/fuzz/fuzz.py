import random
import json

#퍼징할 데이터모음 txt 불러오기
def get_dic(fname,dir="./dictionary/"):
	f = open(dir+fname,"r",encoding="utf8")
	lines = f.read().splitlines() 

	while lines.count("") > 0:
		lines.remove("")	
	
	return lines

#get_dic으로 읽어온 데이터에서 랜덤으로 값 부여
def set_method(list_method):
	method_rand = list_method[ random.randrange(0,2) ]
	return method_rand

def set_dir(list_dir):
	dir_num = random.randrange(1,5)
	dir_rand =""

	for i in range(1,dir_num+1):
		dir_rand +="/"+list_dir[random.randrange(0,len(list_dir))]

	return dir_rand


def set_pagenm(list_pagenm):
	pagenm_rand = list_pagenm[ random.randrange(0,len(list_pagenm))]
	return pagenm_rand

def set_host(list_host):
	host_rand = list_host[ random.randrange(0,len(list_host))]
	return host_rand

def set_accept(list_accept):
	accept_rand = list_accept[ random.randrange(0,len(list_accept))]
	return accept_rand

def set_useragent(list_useragent):
	useragent_rand = list_useragent[ random.randrange(0,len(list_useragent))]
	return useragent_rand

def set_referer(list_referer):
	referer_rand = list_referer[ random.randrange(0,len(list_referer))]
	return referer_rand

def set_acceptencoding(list_acceptencoding):
	acceptencoding_rand = list_acceptencoding[ random.randrange(0,len(list_acceptencoding))]
	return acceptencoding_rand

def set_acceptlanguage(list_acceptlanguage):
	acceptlanguage_rand = list_acceptlanguage[ random.randrange(0,len(list_acceptlanguage))]
	return acceptlanguage_rand

def set_connection(list_connection):
	connection_rand = list_connection[ random.randrange(0,len(list_connection))]
	return connection_rand

def set_cookie(list_cookie):
	cookie_num = random.randrange(1,7)
	cookie_rand =""

	for i in range(1,cookie_num+1):
		cookie_rand += list_cookie[random.randrange(0,len(list_cookie))] +"; "

	return cookie_rand[:-3]	#마지막 ; 를 빼주기위해

def set_contenttype(list_contenttype):
	contenttype_rand = list_contenttype[random.randrange(0,len(list_contenttype))]
	return contenttype_rand

#type=1 : url파라미터
#type=2 : urlencoded
def set_data(list_varable_name,list_varable_value):

	variable_num = random.randrange(1,8)
	variable_rand = ""
	for i in range(1,variable_num+1):
		variable_rand += list_varable_name[random.randrange(0,len(list_varable_name))]+"="+list_varable_value[random.randrange(0,len(list_varable_value))]+"&"

	return variable_rand[:-1]

def set_data_FS(list_varable_name):

	FS_list=["%n","%d","%i","%u","%o","%x","%X","%f","%F","%e","%E","%g","%G","%a","%A","%c","%s","%p"]
	variable_num = random.randrange(1,8)
	variable_len = random.randrange(4,30)
	variable_value = ""
	#포맷스트링 데이터 만들기
	for i in range(1, int((variable_len+1)/2) ):
		variable_value += FS_list[random.randrange(0,len(FS_list))]
		variable_value += "%n"
		variable_value += FS_list[random.randrange(0,len(FS_list))]

	
	variable_rand = ""	#최종 데이터

	for i in range(1,variable_num+1):
		variable_rand += list_varable_name[random.randrange(0,len(list_varable_name))]+"="+variable_value+"&"

	return variable_rand[:-1]

def set_data_FD(list_varable_name,list_variable_value_FD):
	FD_list=[["../","./"],["%2e%2e%2f","%2e%2f"],["%252e%252e%252f","%252e%252f"]]

	encoding = random.randrange(0,3)

	variable_num = random.randrange(1,8)

	variable_len = random.randrange(3,8)
	variable_value = ""

	for i in range(1,variable_len+1):
		variable_value += FD_list[encoding][random.randrange(0,2)]

	variable_value += list_variable_value_FD [random.randrange( 0,len(list_variable_value_FD) ) ]


	#FD 데이터만들기
	variable_rand = ""
	for i in range(1, variable_num+1):
		variable_rand += list_varable_name[random.randrange(0,len(list_varable_name))] + "="+variable_value+"&"

	return variable_rand[:-1]

def set_packet(default_key,type,Howmanytime):

	list_method = get_dic("method.txt")
	list_dir = get_dic("dir.txt")
	list_pagenm = get_dic("pagenm.txt")
	list_host = get_dic("host.txt")
	list_accept = get_dic("accept.txt")
	list_useragent = get_dic("useragent.txt")
	list_referer = get_dic("referer.txt")
	list_cookie = get_dic("cookie.txt")
	list_contenttype = get_dic("contenttype.txt")
	list_acceptencoding = get_dic("acceptencoding.txt")
	list_acceptlanguage = get_dic("acceptlanguage.txt")
	list_connection = get_dic("connection.txt")
	list_varable_name = get_dic("variable_name.txt")
	list_varable_value = get_dic("variable_value.txt")


	input_dict = read_jsonfile("user_input.txt")
	#input값 , ipnut이없으면 ""으로 초기화
	method_input = input_dict["method"]
	dir_input = input_dict["dir"]
	pagenm_input = input_dict["pagenm"]
	host_input = input_dict["host"]
	accept_input = input_dict["accept"]
	useragent_input = input_dict["useragent"]
	referer_input = input_dict["referer"]
	cookie_input = input_dict["cookie"]
	contenttype_input = ""
	acceptencoding_input = input_dict["acceptencoding"]
	acceptlanguage_input = input_dict["acceptlanguage"]
	connection_input = input_dict["connection"]
	data_body_input = input_dict["data"]
	data_url_input = input_dict["data"]
	contentlength_input = ""

	#공격유형 데이터들 설정

	print("XI,LI,FS,FD유형은 'content-type: application/x-www-form-urlencoded' 로 고정됩니다.")
	contenttype_input = "application/x-www-form-urlencoded"

	print("XI,LI,FS,FD유형은 정의된 data를 사용합니다. \n\n")
	if type =="XI":
		list_variable_value_XI = get_dic("variable_value_XI.txt")
		data_url_input = set_data(list_varable_name,list_variable_value_XI)
		data_body_input = set_data(list_varable_name,list_variable_value_XI)
	elif type == "LI":
		list_variable_value_LI = get_dic("variable_value_LI.txt")
		data_url_input = set_data(list_varable_name,list_variable_value_LI)
		data_body_input = set_data(list_varable_name,list_variable_value_LI)
	elif type =="FS":
		data_url_input = set_data_FS(list_varable_name)
		data_body_input = set_data_FS(list_varable_name)

	elif type =="FD": #FD는 encoding유형에 따라 다르게 해줘야해서 아래의 for문을 돌도록 하였음
		list_variable_value_FD = get_dic("variable_value_FD.txt")
		data_url_input = set_data_FD(list_varable_name,list_variable_value_FD)
		data_body_input = set_data_FD(list_varable_name,list_variable_value_FD)


	packet_list =[]
	#퍼저데이터 생성
	for i in range(1,Howmanytime):

		if type =="FD": #FD는 encoding유형에 따라 다르게 해줘야해서 for문을 돈다
			list_variable_value_FD = get_dic("variable_value_FD.txt")
			data_url_input = set_data_FD(list_varable_name,list_variable_value_FD)
			data_body_input = set_data_FD(list_varable_name,list_variable_value_FD)

		#input값들 넣는다 , input값이 없으면 ""이다.
		method = method_input
		dir = dir_input
		pagenm = pagenm_input
		data_url = data_url_input
		host = host_input
		accept = accept_input
		useragent = useragent_input
		referer = referer_input
		cookie = cookie_input
		contenttype = contenttype_input
		acceptencoding = acceptencoding_input
		acceptlanguage = acceptlanguage_input
		connection = connection_input
		data_body = data_body_input
		contentlength = contentlength_input
		


		if default_key[type]["METHOD"]:	#default_key.txt를 보고 해당부분 넣을지 말지 결정

			#input값이 없을때
			if method == "":		
				method = set_method(list_method)
				method_bak = method
				method +=" "

			#input값이 잇을떄
			else:
				method_bak = method
				method +=" "
		else:							#default_key.txt에서 값이 0이면 ""로해서 packet에 포함 X
			method_bak = method
			method = ""

		#URL파라미터 데이터 , POST BODY데이터 2개중에 하나 결정하는 RANDOM
		#0이면 url파라미터데이터 , 1이며녀 POST BODY데이터를 쓰는거로 결정
		if method_bak == "POST":
			body_or_url = random.randrange(0,2)

		else: #GET일때는 무조건 url파라미터 데이터이므로 0 
			body_or_url = 0

		
		if default_key[type]["DIR"]:
			if dir == "":
				dir = set_dir(list_dir)
				dir +="/"
			else:
				dir +="/"
		else:
			dir = ""

		if default_key[type]["Pagenm"]:
			if pagenm == "":
				pagenm = set_pagenm(list_pagenm)
			else:
				pagenm = pagenm
		else:
			pagenm = ""

		if default_key[type]["DATA_URL"] and body_or_url ==0:		
			if data_url == "":
				data_url = "?"
				data_url += set_data(list_varable_name,list_varable_value)
			else:
				data_url ="?"+data_url
		else:
			data_url = ""
			
		if default_key[type]["HOST"]:			
			if host == "":
				host = set_host(list_host)
				host = "\nHOST: "+host
			else:
				host = "\nHOST: "+host
		else:
			host = ""
		
		if default_key[type]["Accept"]:		
			if accept == "":
				accept = set_accept(list_accept)
				accept = "\nAccept: "+accept
			else:
				accept = "\nAccept: "+accept
		else:
			accept = ""
		
		if default_key[type]["User-Agent"]:	
			if useragent == "":
				useragent = set_useragent(list_useragent)
				useragent = "\nUser-Agent: "+useragent
			else:
				useragent = "\nUser-Agent: "+useragent
		else:
			useragent = ""

		if default_key[type]["Referer"]:	
			if referer == "":
				referer = set_referer(list_referer)
				referer = "\nReferer: "+referer
			else:
				referer = "\nReferer: "+referer
		else:
			referer = ""

		if default_key[type]["Cookie"]:					
			if cookie == "":
				cookie = set_cookie(list_cookie)
				cookie = "\nCookie: "+cookie
			else:
				cookie = "\nCookie: "+cookie
		else:
			cookie = ""

		if method_bak =="POST" and body_or_url ==1:			
			if contenttype == "":
				contenttype = set_contenttype(list_contenttype)
				contenttype = "\nContent-type: "+contenttype
			else:
				contenttype = "\nContent-type: "+contenttype
		else:
			contenttype = ""

		if default_key[type]["Accept-Encoding"]:		
			if acceptencoding == "":
				acceptencoding = set_acceptencoding(list_acceptencoding)
				acceptencoding = "\nAccept-Encoding: "+acceptencoding
			else:
				acceptencoding = "\nAccept-Encoding: "+acceptencoding
		else:
			acceptencoding = ""
		
		if default_key[type]["Accept-Language"]:	
			if acceptlanguage == "":
				acceptlanguage = set_acceptlanguage(list_acceptlanguage)
				acceptlanguage = "\nAccept-Language: "+acceptlanguage
			else:
				acceptlanguage = "\nAccept-Language: "+acceptlanguage
		else:
			acceptlanguage = ""


		if default_key[type]["Connection"]:	
			if connection == "":
				connection = set_connection(list_connection)
				connection = "\nConnection: "+connection
			else:
				connection = "\nConnection: "+connection
		else:
			connection = ""

		if method_bak == "POST" and body_or_url ==1:			
			if data_body == "":
				data_body = set_data(list_varable_name,list_varable_value)
				data_body = "\n\n"+data_body
			else:
				data_body = "\n\n"+data_body
		else:
			data_body = ""

		if method_bak == "POST" and body_or_url ==1:			
			contentlength = len(data_body)
			contentlength = "\nContent-Length: "+ str(contentlength)
	
		packet = method + dir + pagenm + data_url + " HTTP/1.1"	#GET /dir1/dir2/pagename.asp?value1=abc&value2=bbb HTTP/1.1
		packet += host												
		packet += accept												
		packet += useragent												
		packet += referer												
		packet += cookie												
		packet += contenttype	
		packet += contentlength											
		packet += acceptencoding												
		packet += acceptlanguage												
		packet += connection												
		packet += data_body

		packet_list.append(packet)
	
	return packet_list
		
def read_jsonfile(file):
	
	f = open(file,"r",encoding="utf-8")
	index_dict = json.load(f)
	
	return index_dict

default_key = read_jsonfile("default_key.txt")




print("사용자가 직접 데이터를 입력하고싶으시면. user_input.txt에 값을 넣어주세요.")
print("값을 설정하지 않을시 default데이터로 퍼저가 생성됩니다.")

type = input("공격유형을 입력하세요 ex)입력 : FS \n입력 : ")
Howmanytime = input("생성할 패킷수를 입력하세요 ex)입력 : 1998 \n입력 : ")

#type ="FD"
#Howmanytime =10
packet_list = set_packet(default_key,type,int(Howmanytime))

for i in packet_list:
	print(i+"\n")
