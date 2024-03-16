
--사용방법---
1. 사용자 정의 인풋 넣기
값을 넣지 않으면 도구에서 제공하는 기본 dictionary로 퍼저를 생성합니다.
먄약 사용자가 원하는 데이터를 고정해서 넣고 싶으시면 user_input.txt 에 값을 넣으면됩니다.
user_input.txt는 아래와같은형식이고 
{
    "method":"",
    "dir":"",
    "pagenm":"",
    "host":"",
    "accept":"",
    "useragent":"",
    "referer":"",
    "cookie":"",
    "acceptencoding":"",
    "acceptlanguage":"",
    "connection":"",
    "data":""
}

HOST가 WWW.NAVER.COM으로 , data는 var1=abcd&var2=1234로 고정된 패킷을 생성하고싶다면 아래와같이 작성하면됩니다.
{
    "method":"",
    "dir":"",
    "pagenm":"",
    "host":"WWW.NAVER.COM",
    "accept":"",
    "useragent":"",
    "referer":"",
    "cookie":"",
    "acceptencoding":"",
    "acceptlanguage":"",
    "connection":"",
    "data":"var1=abcd&var2=1234"
}

2.공격유형 입력하기
fuzz.py를 실행하였을때 입력하면됩니다.
현재 4개의 유형에 대해 개발이 완료되었고
"FS" ,"FD", "XI","LI" 이 4개중 한개를 입력하면됩니다.

3.패킷 생성수 정하기
fuzz.py를 실행하였을때 입력하면됩니다.
퍼저로 생성하는 패킷수를 정합니다.


--코드 설명--
set_packet() : 랜덤 패킷을 생성하는 함수입니다.
				랜덤패킷을 생성한후 packet_list에 넣습니다.
				최종 반환값은 packet_list입니다.
get_dic() : /dictionary/ 폴더에잇는 딕셔너리 데이터를 읽어들입니다.

