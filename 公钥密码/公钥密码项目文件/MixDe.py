def get_code(text):
    fp=open(text,'r',encoding='utf-8')
    dd=fp.read()
    fp.close()
    
    m=[]
    i=0
    
    while(len(dd)):
        if dd[i]!='|':
            i=i+1
        else:
            m.append(eval(dd[:i]))
            dd=dd[i+1:]
            i=0
    return m    
def set_code(text,connect):
    print("\n将把操作的数据写入文件\n")
    print(text)
    
    try:        
        fp=open(text,'w',encoding='utf-8')
        for i in connect:
            fp.write(chr(i))    
        fp.close() 
        print("\n写入成功！")
    except:
        print("\n写入失败。") 
def Inverse(b,a=52):
    X=[1,0,a]
    Y=[0,1,b]
    if b==0:
        return None;
    
    while Y[2]!=1 and Y[2]!=0:
        Q= X[2]/Y[2] > 0 and int(X[2]/Y[2]) or -int(X[2]/Y[2])
        T=[X[0]-Q*Y[0],X[1]-Q*Y[1],X[2]-Q*Y[2]]
        X=[Y[0],Y[1],Y[2]]
        Y=[T[0],T[1]%a,T[2]]
    return Y[2]==1 and Y[1] or 0
def de_code_RSA(c):
    k=[705, 1081]
    m=[]
    for i in c:
        m.append((i**k[0])%k[1])
    
    return m
def de_code_MH(c):
    k=[1, 3, 5, 11, 21, 44, 87, 701, 43, 1590]
    W=k[8]
    M=k[9]
    k=k[:-2]
    d=Inverse(W,M)
    m=[]
    for i in c:
        j=0
        temp=(i*d)%M
        if temp-k[7]>=0:
            j+=1
            temp=temp-k[7]
        
        if temp-k[6]>=0:
            j+=2
            temp=temp-k[6]
        
        if temp-k[5]>=0:
            j+=4
            temp=temp-k[5]
        
        if temp-k[4]>=0:
            j+=8
            temp=temp-k[4]
        
        if temp-k[3]>=0:
            j+=16
            temp=temp-k[3]
        
        if temp-k[2]>=0:
            j+=32
            temp=temp-k[2]
        
        if temp-k[1]>=0:
            j+=64
            temp=temp-k[1]
        
        if temp-k[0]>=0:
            j+=128
            temp=temp-k[0]
        m.append(j)
    return m 
        
set_code('RSA.txt',de_code_RSA(get_code('RSA.txt')))
set_code('MH.txt',de_code_MH(get_code('MH.txt')))