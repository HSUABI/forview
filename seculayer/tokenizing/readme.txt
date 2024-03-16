test.json : 테스트 데이터
test_word.json : 테스트데이터를 word만뽑아서 다시 json으로 넣은것
tk.py : test.json데이터를 읽고 word를 뽑아서 test_word.json에 파일을 씁니다.
tknize.py : word뽑는 함수가 있습니다.
	DATA_word(data)		: isalpha()를 사용해서 영어,한글 문자가 있을때 단어로 뽑습니다.
	COOKIE_word(data)	: DATA_word와 똑같은 동작을하지만 base64decode 과정만 없습니다.
	URL_word(url)		: "/","\"로 split을 한후 맨마지막에 file.asp같은 확장자가 있을경우 이를 .으로 split하여 word를 뽑습니다.