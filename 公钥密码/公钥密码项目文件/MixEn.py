def get_code(text):
    print(text)
    fp=open(text,'r',encoding='utf-8')
    dd=fp.read()
    fp.close()
    m=[]
    
    print("\n载入要操作的字符串")
    
    for i in dd:
        m.append(ord(i))
    
    print("\n载入完成")
    
    return m
def set_code(text,connect):
    print("\n将把操作的数据写入文件")
    print(text)
    
    try:        
        fp=open(text,'w')
        for i in connect:
            fp.write(str(i)+'|')
        fp.close() 
        print("\n写入成功！")
    except:
        print("\n写入失败。") 

    pass
def en_code_MH(m):
    k=[43, 129, 215, 473, 903, 302, 561, 1523, 1590]
    M=k[8]
    k=k[:8]
    c=[]
    for i in m:
        temp=0
        temp = temp+k[0]*((int)(i/128))
        temp = temp+k[1]*((int)(i/64)%2)
        temp = temp+k[2]*((int)(i/32)%2)
        temp = temp+k[3]*((int)(i/16)%2)
        temp = temp+k[4]*((int)(i/8)%2)
        temp = temp+k[5]*((int)(i/4)%2)
        temp = temp+k[6]*((int)(i/2)%2)
        temp = temp+k[7]*(i%2)
        c.append(temp%M)
        
    return c   
def en_code_RSA(m):
    k=[89, 1081]
    c=[]
    for i in m:
        c.append((i**k[0])%k[1])
    
    return c

set_code('RSA.txt',en_code_RSA(get_code('Alan Turing.txt')))
set_code('MH.txt',en_code_MH(get_code('Alan Turing.txt')))