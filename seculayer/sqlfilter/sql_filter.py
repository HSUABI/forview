import copy


class tree :
    def __init__(self,value):
        self.value = value
        self.childnum = 0
        self.child = []
        self.right = None

def inorder(t):
    if t is not None:
        for i in range(0,childnum):
            inorder(t.child[childnum])
        print(t.value+" ",end='')
        inorder(t.right)

def constructTree(string):
    stack = []
    subtree = []
    commanum = 0
    sql = string.split()
    sql_copy = copy.deepcopy(sql)
    sql2copy = copy.deepcopy(sql)
#    for i in sql2copy:
#        if check(i) is 0:
#            stack.append(i)
#        elif check(i) is 1:
#            commanum += 1
#        elif check(i) is 2:
#            
#    parse(sql_copy)
    

def parse(sql):
    flag = 0
    commaindex=[]
    subquery=[]
    for i in sql:
        if i is ",":
            commaindex.append(sql.index(i))
        if i is "(":
            start = sql.index(i)
            end = subparse(sql,start)
            subquery = sql[int(start)+1:end]
            sql[start] = subquery
            del sql[start+1:end+1]
    commaindex.reverse()
    for i in commaindex:
        del sql[i]

    print(sql)

    
def subparse(sql,start):
    count = 1
    for i in range(start+1,len(sql)):
        
        l = sql[i]
        if l is "(":
            count += 1
        if l is ")":
            count -= 1
        if count is 0:
            return i

def splitcheck(sql):
    slist=[]
    backup = []
    for i in sql:
        for l in i:
            if len(i) is 1 :
                continue
            elif l is ",":
                slist.append([sql.index(i),i.index(l)])
            elif l is "(":
                slist.append([sql.index(i),i.index(l)])
            elif l is ")":
                slist.append([sql.index(i),i.index(l)])
                
    slist.reverse()
    for i in slist:
        backup = [sql[i[0]][:i[1]],sql[i[0]][i[1]],sql[i[0]][i[1]+1:]]
        del sql[i[0]]
        backup.reverse()
        for l in backup:
            if l is '':
                continue
            else:
                sql.insert(i[0],l)


def by_assign_check(sql):
    bylist = []
    for i in sql:
        if isinstance(i,list):
            continue
    if i.lower() == "order":
        if sql[sql.index(i)+1].lower() == 'by':
            print (sql.index(i))
            bylist.append(sql.index(i))
    if i.lower() == "group":
        if sql[sql.index(i)+1].lower() == "by":
            print(sql.index(i))
            bylist.append(sql.index(i))
    bylist.reverse()
    for i in bylist:
        sql[i] = sql[i]+" "+sql[i+1]
    del sql[i+1]


'''            
string = "a, e( b , c ) d"
sql = string.split()
print("string : "+string)
print("split string : "+str(sql))
#subparse(sql,1)
splitcheck(sql)
print(sql)
parse(sql)
'''
