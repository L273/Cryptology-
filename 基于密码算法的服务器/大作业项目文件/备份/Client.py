import socket
import threading
import time
import random

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓IDEA_En代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
# 8位一个字符的单位编排

#模加运算
def plus(x,y):
    return x<0 or y<0 and None or (x+y)%(2**16)

#模乘运算
#0，0的情况特殊照顾
def mul(x,y):
    if x<0 or y<0:
        return None
    else:
        pass
    
    if x==0 and y==0:
        x=2**16
        y=2**16
    elif x==0:
        x=2**16
    elif y==0:
        y=2**16
    else:
        pass
    
    return (x*y)%(2**16+1)==2**16 and 0 or (x*y)%(2**16+1)

#异或运算，结果mod 2的16次方    
def diff(x,y):
    return x<0 or y<0 and None or (x^y)%(2**16)

def str_16num(m):
    n=[]
    for i in range(0,len(m),2):
        n.append(ord(m[i])*(2**8)+ord(m[i+1]))
    return n

#循环左移25位
def loop_25(num):
    temp_low=num>>(128-25)
    num=num<<25
    num=num&(2**128-1)
    return  num+temp_low
    
# 密钥拓展    
def get_long_key(key):
    K=[]
    while(len(key)<16):
        key = key + " "
    key=key[:16]
    while(len(K)<52):
        
        #取数据
        for i in range(0,16,2):
            K.append(ord(key[i])*(2**8)+ord(key[i+1]))
        
        #循环左移25位
        key_num=0
        for i in key:
            key_num = key_num*(2**8) + ord(i)
        key_num=loop_25(key_num)
        
        #重构key，以便下一次循环
        key=""
        for i in range(1,17):
            key = key + chr((key_num>>(128-i*8))%(2**8))
        
    K=K[:52] #会取到56个key，所以就要截取
    
    return K
        
def IDEA_EN(m,k):
    # 密钥转换
    key=get_long_key(k)
    
    # 数据转换
    W=str_16num(m)
    
    #8轮的IDEA计算
    for i in range(0,48,6):
        K=[]
        K.append(key[i])
        K.append(key[i+1])
        K.append(key[i+2])
        K.append(key[i+3])
        K.append(key[i+4])
        K.append(key[i+5])
        
        W[0]=mul(W[0],K[0])
        W[1]=plus(W[1],K[1])
        W[2]=plus(W[2],K[2])
        W[3]=mul(W[3],K[3])
   
        Oper_1=diff(W[0],W[2])
        Oper_2=diff(W[1],W[3])
        
        Oper_1=mul(Oper_1,K[4])
        Oper_2=plus(Oper_1,Oper_2)

        Oper_2=mul(Oper_2,K[5])
        Oper_1=plus(Oper_2,Oper_1)
        
        W[0]=diff(W[0],Oper_2)
        temp=W[1]
        W[1]=diff(W[2],Oper_2)
        W[2]=diff(temp,Oper_1)
        W[3]=diff(W[3],Oper_1)
    
    
    K=[]
    for i in range(48,52):
        K.append(key[i])
        
    #输出变换
    Y=[]
    Y.append(mul(W[0],K[0]))
    Y.append(plus(W[2],K[1]))
    Y.append(plus(W[1],K[2]))
    Y.append(mul(W[3],K[3]))
    
    #转换成16进制字符串后返回
    
    result=""
    for i in Y:
        i=str(hex(i)).replace('0x','')
        while(len(i)<4):
            i = '0' + i
        result = result + i
    
    return result

# print(IDEA_EN("abcdefgh",'abcdefghijklmnop'))       

'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑IDEA_En代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

#针对发送的补充，由于IDEA64一组数据，所以我们要对大的msg进行切片，小的msg进行补齐。
def to_IDEA_64(msg):
    #ASCII编码，一个8位，所以64的判断，就是长度8的ASCII字符串判断
    while(len(msg)<8 or len(msg)%8!=0):
        msg = msg + ' '
        #不够末尾补" " &nbsp

    return msg

#IDEA加密长度位64背书的字符
def IDEA_MSG(msg,key):
    new_msg=""
    msg=to_IDEA_64(msg)
    while(len(msg)):
        new_msg=new_msg + IDEA_EN(msg[:8],key)
        msg=msg[8:]
    return new_msg


'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓MD5代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
T=[0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
	0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
	0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
	0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
	0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
	0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
	0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
	0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]

def get_code(dd):
    m=[]
    for i in dd:
        if(ord(i)<128):
            m.append(ord(i))
    
    return m

def section(m):
    length=(len(m)*8)%(2**64)
    if(len(m)%64>56):
        m.append(0x80)
        if(len(m)%64!=0):
            m.append(0x00)
            #补齐到512
        for i in range(56):
            m.append(0x00)
            #补上448
    elif(len(m)%64==56):
        m.append(0x80)
        for i in range(63):
            m.append(0x00)
        #448的情况为填充512的数据
    else:
        m.append(0x80)
        while(len(m)%64!=56):
            m.append(0x00)
        #直接补齐到448
    
    #补最后的64位，由于Step中32位的小端转化，所以，这里切片后就不小端转换了。
    high=(int)(length/(2**32))
    low=(int)(length%(2**32))
    temp=[[]for i in range(2)]

    while(low%256!=0):
        temp[0].append(low%256)
        low=low>>8
    
    while(high%256!=0):
        temp[1].append(high%256)
        high=high>>8
    
    for i in range(len(temp)):
        while(len(temp[i])<4):
            temp[i].append(0x00)
    for i in temp:
        for j in i:
            m.append(j)
    return m
        
def not_(x):
    return 0xffffffff-x

def g(b,c,d,i):
    if i==0:
        return (b&c)|((not_(b))&d)
    elif i==1:
        return (b&d)|(c&not_(d))
    elif i==2:
        return b^c^d
    elif i==3:
        return c^(b|not_(d))

def X_k(i,j):
    if i==0:
        return j
    elif i==1:
        return (1+5*j)%16
    elif i==2:
        return (5+3*j)%16
    elif i==3:
        return (7*j)%16

def cls(temp,i,j):
    tab=[
    [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22],
    [5,9,14,20 ,5,9,14,20 ,5,9,14,20 ,5,9,14,20],
    [4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23],
    [6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
    ]
    temp_low=temp>>(32-tab[i][j])
    temp=(temp<<tab[i][j])&0xffffffff
    temp=temp+temp_low
    return temp

def One_512(m,A_D):
    step=[]
    for i in range(16):
        step.append(m[4*i:4*i+4])
    for i in range(len(step)):
        #大小端转换
        step[i].reverse()
   
    a=A_D[0]
    b=A_D[1]
    c=A_D[2]
    d=A_D[3]
    for i in range(4):
        for j in range(16):
            temp=g(b,c,d,i)
            temp=(a+temp)%(2**32)
            
            temp_32=0
            for y in step[X_k(i,j)]:
                temp_32 = temp_32*(2**8)+y
            temp=(temp+temp_32)%(2**32) 
            
            temp=(temp+T[16*i+j])%(2**32)
            temp=cls(temp,i,j)
            temp=(temp+b)%(2**32)
            
            result_a=d
            result_b=temp
            result_c=b
            result_d=c
            
            a=result_a
            b=result_b
            c=result_c
            d=result_d
    

    a=(a+A_D[0])%(2**32)
    b=(b+A_D[1])%(2**32)
    c=(c+A_D[2])%(2**32)
    d=(d+A_D[3])%(2**32)
    
    A_D=[a,b,c,d]
    
    return A_D

def re_hash(hash):   
    #因为是小端存储，返回的时候，要再度使用reverse，以便人的读取
    j=0
    re_hash=""
    for i in hash:
        while(i!=0):
            j = j + i%256;
            j=j<<8;
            i=i>>8;
        j=j>>8
        j_temp=str(hex(j)).replace('0x','')
        while(len(j_temp)<8):
            #专门对付j开头是0的情况
            j_temp = '0' + j_temp
        re_hash = re_hash + j_temp
        j=0
    return re_hash
    
def MD5(m):
    
    #大小端转换
    A=0x67452301 #0x01234567
    B=0xefcdab89 #0x89abcdef
    C=0x98badcfe #0xfedcba98
    D=0x10325476 #0x76543210
    
    hash=[A,B,C,D]
    m=section(m)
    
    while(len(m)):
        hash=One_512(m[:64],hash)
        m=m[64:]
    
    
    #因为是小端存储，返回的时候，要再度使用reverse，以便人的读取
    
    return re_hash(hash)
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑MD5代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''


'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓RSA签名代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
#对MD5 即HASH值进行签名，使用私钥(32个16进制数，每个数值都进行签名)
def de_code_RSA(c):
    k=[23, 187]
    m=""
    for i in c:
        i=int(i,16)
        
        i=(i**k[0])%k[1] #对每个16进制数进行签名
        
        m = i>16 and m+hex(i)[2:] or m+'0'+hex(i)[2:]
    return m


#对MD5 即HASH值进行签名，使用私钥(32个16进制数，每个数值都进行签名)
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑RSA签名代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓密钥协商代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
def get_DH_KEY(socket_client):
    p=97
    a=5
    key=""
    while(len(key)<16):
        Xa=(int(time.time())%15)*int(random.random()*100)
        Ya=str(a**Xa)
        socket_client.send(Ya.encode('utf-8'))
        Yb = socket_client.recv(1024).decode('utf-8')
        Yb = eval(Yb)
        K_temp=(Yb**Xa)%p
        key = key + chr(K_temp)
        
    return key

''' 
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑密钥协商代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓RSA加密K代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
def en_RSA(key):
    k=[7, 187]
    c_key=""
    for i in key:
        i=ord(i)
        
        i=(i**k[0])%k[1] #对每个ASCII数值进行加密
        
        c_key = c_key + chr(i)
    return c_key

'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑RSA加密K代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''
#发送数据给Server，用于加密sd
def client():
    server=("localhost",9897)
    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_client.connect(server)
    
    print("="*50)
    print("Connect Server:" + str(server))
    key=get_DH_KEY(socket_client)
    c_key=en_RSA(key)
    while(True):
        print("-"*50)
        data=input("请输入数据：  ")
        data=data.rstrip()+de_code_RSA(MD5(get_code(data.rstrip())))
        data=IDEA_MSG(data,key)
        data=data+c_key
        socket_client.send(data.encode('utf-8'))
  
    
client()
