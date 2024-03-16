import base64

def tknize_FUP(PAYLOAD):
	
	for packet in PAYLOAD:	#payload에 패킷이 여러개있을수있어서 for문돌림
	
		# '/' '\' 이런거 한꺼번에 split해주기
		URL = packet["URL"]
		URL = URL.replace("/","split_word")
		URL = URL.replace("\\","split_word")
		packet["URL"] = URL.split("split_word")
		
		file = packet["URL"][-1]	#/abc/acb/file.txt , url에서 file.txt를 가져오는거
		file = file.split(".")

		#file.txt를 file , txt로 나누기
		del packet["URL"][-1]
		packet["URL"] = packet["URL"] + file


	return PAYLOAD

def tknize_UUA(PAYLOAD):
	
	for packet in PAYLOAD:	#payload에 패킷이 여러개있을수있어서 for문돌림

		# '/' '\' 이런거 한꺼번에 split해주기
		URL = packet["URL"]
		URL = URL.replace("/","split_word")
		URL = URL.replace("\\","split_word")
		packet["URL"] = URL.split("split_word")
		
		file = packet["URL"][-1]	#/abc/acb/file.txt , url에서 file.txt를 가져오는거
		file = file.split(".")

		#file.txt를 file , txt로 나누기
		del packet["URL"][-1]
		packet["URL"] = packet["URL"] + file


	return PAYLOAD


def tknize_FDOWN(PAYLOAD):
	
	for packet in PAYLOAD:	#payload에 패킷이 여러개있을수있어서 for문돌림
		
		# '/' '\' 이런거 한꺼번에 split해주기
		URL = packet["URL"]
		URL = URL.replace("/","split_word")
		URL = URL.replace("\\","split_word")
		packet["URL"] = URL.split("split_word")

		file = packet["URL"][-1]	#/abc/acb/file.txt , url에서 file.txt를 가져오는거
		file = file.split(".")

		#file.txt를 file , txt로 나누기
		del packet["URL"][-1]
		packet["URL"] = packet["URL"] + file

		# '/' '\' 이런거 한꺼번에 split해주기
		DATA = base64.b64decode(packet["DATA"][0]).decode("utf-8")
		DATA = DATA.replace("/","split_word")
		DATA = DATA.replace("\\","split_word")
		packet["DATA"] = DATA.split("split_word")

	return PAYLOAD


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

#DATA_word와 똑같은 역할
def COOKIE_word(data):
	data_only_word=[]
	word=""
	for string in data:
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

#COOKIE_word함수와 똑같지만 함수명이상해서 함수명을 바꿈
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