
'''
원본 : SELECT * FROM t1 JOIN t2 USING (j);

함수거친후 : select * fromspace!@#t1space!@#joinspace!@#t2space!@#space!@#using (j);

replace로해서 다시 공백 만들기 : select * from t1 join t2  using (j);

'''
def join_parse(string):

	join_commands=["natrual left outer join","natural right outer join","natural left join","natural right join","inner join","cross join","straight_join","left join","right join","left outer join","right outer join","natural join","join"]
	index_join_start = 0
	chk=0
	next_join = -1

	#join command가 아무것도 없으면 그냥 return
	for join_command in join_commands:
		if join_command in string:
			break
		chk+=1
	if chk==len(join_commands):
		return string
	
	#join문 뒤에 나오는 것들을 검사한다. 그후에 그 위치를 index_join_end에넣는다.
	if "on" in string:
		index_on = string.index("on")
		index_join_end = index_on

	elif "using" in string:
		index_using = string.index("using")
		index_join_end = index_using

	elif "where" in string:
		index_where = string.index("where")
		index_join_end = index_where

	elif "order by" in string:
		index_order = string.index("order by")
		index_join_end = index_order

	elif "group by" in string:
		index_group = string.index("group by")
		index_join_end = index_group

	else: #SELECT * FROM t1 NATURAL JOIN t2 이런 경우 일때
		index_join_end = -1


	#함수 처음 실행할때 실행
	#join문시작을 FROM바로 뒤로 잡음
	if "from" in string:
		index_from = string.index("from")
		index_join_start = index_from+len("from")

	#함수 재귀해서 2번째이상 실행될때
	#join문시작을 inner join , join 같은 명령어 시작부분으로 잡음 
	else:
		for join_command in join_commands:
			if join_command in string:
				index_join_start = string.index(join_command)
				break

	#이건 재귀문 돌릴지 말지 체크하는 부분
	#첫번째 join문 다음에 나오는 두번째 join문의 index를 찾는다. 그리고 있으면 next_join에 값을 넣는다.
	#이부분을 A부분이라 칭함
	for join_command in join_commands:
		if join_command in string[index_join_end:]:
			next_join = string[index_join_end:].index(join_command) 
			break

	#공백을 없애고 한뭉터기로 묶을 범위를 지정함.  join문 부분을 한뭉터기로 묶음
	join_syntax = string[index_join_start:index_join_end]

	'''
	#"SELECT * FROM t1 NATURAL JOIN t2"같은 문자열끝에는 공백이없어서 뒤에 공백을 넣어줌
	string = string.replace(join_syntax,join_syntax+" ")
	join_syntax = join_syntax+" "
	join_syntax_nospace = join_syntax.replace(" ","space!@#")
	string = string.replace(join_syntax,join_syntax_nospace)
	index_join_end = string.rfind("space!@#")
	'''

	#공백을 없애주고 한뭉터기로 만들어주기 이건 나중에 replace해서 공백다시 만들어줄수있음
	join_syntax_nospace = join_syntax.replace(" ","space!@#")
	string = string.replace(join_syntax,join_syntax_nospace)
	index_join_end = string.rfind("space!@#")

	#A부분이 돌아서 next_join에 값이 들어오면 아래 return문수행하고 재귀문을 돌린다.
	#어떨때는 +8해야하고 어떨때는 +0해야 딱 맞는데 이부분은 아직 찾지못햇습니다.
	string = string.replace("fromspace!@#","from ")
	fit = 0
	if next_join!=-1:
		#print(string[:index_join_end+next_join])
		return string[:index_join_end+next_join+fit]+join_parse(string[index_join_end+next_join+fit:])

	return string


	


