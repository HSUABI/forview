*ai팀 연동용 함수

파일 : funcs.py
함수명 : pay2json_ai(line,file)
반환값 : dictionary

예제 : pay2json_ai(payload_string.replace("\r\n","\n"),0) 
//2번째 인자는 디버깅용 인자여서 0을 넣어주시면 됩니다.
//payload_string.replace("\r\n","\n") 꼭해주셔야합니다!! "\r\n"을 꼭 "\n"으로 바꾸어주세요.

제가 테스트코드로 paystr2json.py를 만들었습니다. 참고해주세요.
csv파일 하나 읽어서 파싱해서 json파일로 다시 쓰는 코드입니다.
이때는 fwrite을써줘야해서 pay2json_ai를 안쓰고 pay2json을 썻습니다 이점 유의해주십쇼.


*csv 파싱용함수

파일 : funcs.py
함수명 : pay2json(line,file)
반환값 : dictionary를 jsondump한거를 +해서 계속 붙인거

예제 : pay2json( row[payload_index[file]] ,file ) #첫번째 인자에는 페이로드열 , 2번재인자는 파일 이름

main.py에 제가 파싱하는 코드를 작성했습니다.


*별도의 말
parse_3type.py랑 
error/3type.txt는 나중에 readmin작성하겟습니다
시험 2시간남아서 셤끝나고 작성할게요 ㅠㅠ

일단 함수는
tojson_3typeofdata() 이거 중점으로 작성했습니다.
return값은 dict고 인풋값은 string이에요