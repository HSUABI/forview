*코드사용법 
filter.py에서 def filter(line , atk_type)를 사용하시면됩니다.
첫번재 인자 line에는 패킷 데이터가 들어가고 
두번째 인자 atk_type에는 공격유형이 들어갑니다. 
공격유형에 대한 정보는 http://bitly.kr/rPyiSS 여기를 보시거나 filter.py의 198~230라인을 보시면 됩니다. 

filter함수는 패킷을 파싱한후 공격유형에 따라 필요한부분들만 뽑습니다. 그리고 뽑은 값들로 리스트구성하고 이를 반환합니다.
단 중복제거와 word만 뽑는것과 길이만뽑는것은 하지 않았습니다.
만약 하고싶으시다면 960 ~ 980번대 라인을 주석제거 해주시면 감사하겠습니다.




*코드 설명
filter.py : 1유형 , 2유형 ,3유형인지 파악하고 유형에 맞춰서 파싱함
			유형에 맞춰서 파싱한다음 공격유형에 따라서 DATA , URL , COOKIE등을 뽑아 하나의 리스트로 반환함
			1유형으로는 DATA 와 URL만 추출할수있어서 1유형 - XSS공격 에는 COOKIE데이터를 추가하지못하였다. 이와 비슷한 경우가 몇가지 있었습니다. 그래서 이때에는 공격유형 해당하는 KEY들중에서 추출 가능한 KEY들만 뽑고 리스트로 반환했습니다.
			filter.py가 동작하면서 url부분은 URL_word() 함수를 사용해서 리스트에 넣었습니다.
			filter.py를 할때 에러로그를 error폴더안에 넣습니다. 따라서 error폴더를 생성해주어야 filter.py가 정상작동합니다!

			- filter.py가 파싱할때 판단하는 유형 정보

				유형1 	: 맨앞이 / 인 경우
				유형2 	: 풀패킷이 다있는경우
				유형3-1 : 데이터만 따딱 있는경우 (변수=갑&변수=값)
				유형3-2 : 유형2에서 중간에 잘려있는거 COOKIE,HOST같은것들이 있으면 유형 3-2

			- 주석처리한부분
			#리스트로 반환할떄는 [1,"","HELLO","HELLO"] 같은것이있으면 공백을 제거하고 중복제거를하여 [1,"HELLO"]를 반환함
			#빈도수와 길이검사를하기위해서 중복제거는 우선 주석처리하였음
			#WORD만 뽑는것은 Word_only()함수를 사용해 뽑으면 됩니다. 함수명은 Word_only()인데 단어 추출하는 함수입니다. 


main.py : 	log폴더에 있는 csv파일들을 읽고
			rawdata_index.txt를 읽어서 csv파일에서 rawdata가 몇번째 열에 잇는지 확인하고 그 열을 읽어들여
			filter.py의 filter()함수를 이용해서 파싱한후 그 반환값(리스트)을 output폴더에 출력함. 

			중복제거와 word만뽑고싶다면 아래 코드를 활용하면됩니다.
			#중복제거
			#filter_list = list(set(filter_list))	
			#word만 뽑기
			#filter_list = Word_only(filter_list)

getlen.py : output폴더에 있는 출력물들을 읽어서 리스트 원소들의 길이를 알아낸후 그값들로 리스트를 만들어 다시 출력함
			출력물들은 output_len폴더에있음
			ex) ["aa","ccc","dddd"] 를 [2,3,4]이렇게 바꿔줌

*주의사항
가끔씩 utf8에러가 뜨는경우가있습니다.
7시에는 오류뜨다가 껏다키니까 다시 오류가 안뜨네요.

아래 4개의 파일은 정탐오탐 여부가 같이 있는 파일입니다.
그래서 아래 4개의 파일을 파싱할땐 정탐오탐여부를 보고 정탐일때와 오탐일때, 2가지 경우를 나누어서 파싱하고
그결과를 2개의 파일로 나누어 출력하였습니다.

+level1.kisa.sql_injection_total_shuffled.csv
	- level1.kisa.sql_injection_total_shuffled.csv_정탐.txt
	- level1.kisa.sql_injection_total_shuffled.csv_오탐.txt

+ level1.kisa.XSS_total_shuffled.csv
	- level1.kisa.XSS_total_shuffled.csv_오탐.txt
	- level1.kisa.XSS_total_shuffled.csv_정탐.txt

+ SQL_50_param_ext.csv
	- SQL_50_param_ext.csv_정탐.txt
	- SQL_50_param_ext.csv_오탐.txt

+ XSS_50_param_ext.csv
	- XSS_50_param_ext.csv_오탐.txt
	- XSS_50_param_ext.csv_정탐.txt


* 파일 및 폴더 설명
용량이커서 zip으로 한것들 : output , output_len , log

정오탐 분류 데이터_CSV		: UTF-8 CSV로 다시 저장한 폴더
파이오링크 테스트 데이터_CSV	: UTF-8 CSV로 다시 저장한 폴더

output : 	main.py를 돌렸을때 출력물이 저장됨. 
			csv파일을 파싱한 값들이 리스트에 들어가고 이것을 fwrite(str(list))로 하였음

			-파싱된 csv파일들 목록
				#파일이름에 "[xx]~~" 이렇게 []가 들어가면 utf8저장이 안되서 "정탐_level1.kisa.sql_injection(87069).csv" ,"정탐_level1.kisa.sql_injection(133996).csv"이렇게 바꾸었습니다.
				#파이오링크 테스트 데이터\원본데이터\AU_LOG_admin_20190513201614.csv.txt 이 파일에는 빈 리스트만 있습니다.
				AU_LOG_admin_20190513201614.csv 데이터에 user-agent 값이 하나도 없습니다.

				정오탐 분류 데이터\사이버킬체인_레벨1\KISA분류.SQL_INJECTION\정탐_level1.kisa.sql_injection(87069).csv.txt
				정오탐 분류 데이터\사이버킬체인_레벨1\KISA분류.SQL_INJECTION\정탐_level1.kisa.sql_injection(133996).csv.txt
				정오탐 분류 데이터\사이버킬체인_레벨1\KISA분류.XSS\정탐_level1.kisa.XSS - WAPPLES.csv.txt
				정오탐 분류 데이터\사이버킬체인_레벨1\파이오링크 9개 유형\SI\SI_LOG_admin_20190513200225_result_5000 정탐.csv.txt
				정오탐 분류 데이터\사이버킬체인_레벨1\파이오링크 9개 유형\XS\XS_LOG_admin_20190513200927_result_5000 - 정탐.csv.txt
				파이오링크 테스트 데이터\level1.kisa.sql_injection_total_shuffled.csv.txt
				파이오링크 테스트 데이터\level1.kisa.XSS_total_shuffled.csv.txt
				파이오링크 테스트 데이터\level1.parameter_extraction_result\SQL_50_param_ext.csv.txt
				파이오링크 테스트 데이터\level1.parameter_extraction_result\XSS_50_param_ext.csv.txt
				파이오링크 테스트 데이터\원본데이터\AU_LOG_admin_20190513201614.csv.txt
				파이오링크 테스트 데이터\원본데이터\CF_LOG_admin_20190521093748.csv.txt
				파이오링크 테스트 데이터\원본데이터\OC_LOG_admin_20190513195347.csv.txt
				파이오링크 테스트 데이터\원본데이터\PT_LOG_admin_20190513200653.csv.txt
				파이오링크 테스트 데이터\원본데이터\SI_LOG_admin_20190513200225.csv.txt
				파이오링크 테스트 데이터\원본데이터\SS_LOG_admin_20190513201216.csv.txt
				파이오링크 테스트 데이터\원본데이터\XS_LOG_admin_20190513200927.csv.txt


output_len :getlen.py를 돌렸을때 출력물이 저장됨.
			리스트원소들의 길이값들을 새로운 리스트로 만들고 이것을 fwrite(str(list))로 하였음

output_word : main.py를 실행할때 filter_list = Word_only(filter_list) 를 추가해서 word만뽑아 출력하였음

log : '정오탐 분류데이터'와 '파이오링크 테스트 데이터' 폴더에서 정탐 파일들을 모아놓은 폴더

rawdata_index.txt : csv파일별로 rawdata가 위치한 열이 달라서 그것의 정보를 json형식으로 표현하였습니다.

*예시
main.py를 돌렸을때 아래와 같이나옵니다.
["882273%'/**/aND/**/'8'='8"]
["882273%'/**/aND/**/'8%'='3"]
["882273%'\taND\t'8%'='3"]
["turbo'||lower('')||'", '9_56_07_01', 'WEMAKEPRICE,919|gmarketsyndi,ticketmonster|3559,3210|11sthot|11st-1']

getlen.py를 실행하면 위의 결과들을 읽어들여 각원소들의 길이를 확인하여 그 값들을 리스트로 구성합니다.
[25]
[26]
[20]
[20, 10, 67]

getlen.py를 실행하지않고 바로 코드상에서 길이를 구하고싶으시다면 List2length() 함수를 쓰시면 됩니다.
filter_list_len = List2length(filter_list) 코드를 작성하면 길이값 리스트를 구하실수 있습니다.