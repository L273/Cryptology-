import socket 
import threading
import operator #比较字符串
import time
import random

def get_code(dd):
    m=[]
    for i in dd:
        if(ord(i)<128):
            m.append(ord(i))
    
    return m


'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓IDEA_De代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''

# 8位一个字符的单位编排
#   与加密不同的只有拓展密钥，所以，我们就多加一张映射函数to_dekey()就可以了。
#   同时由于输入的值是16进制字符串，所以，就要先将其转化为ASCII字符串后再操作。当然由于是解密，最后的输出得转换成ASCII字符串


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

def six_to_str(m):
    n=""
    #先转换成数字
    m=int(m,16)

    #每8位一读，得到字符串
    #m!=0的情况特别对付末尾为0的情况
    while(m%(2**8)!=0 or m!=0):
        n = chr(m%(2**8)) + n
        m = m>>8
        
    while(len(n)<8):
        #对付16进制字符串开头是00的情况
        n= chr(0) + n
    return n

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

#解密密钥的获取
def to_dekey(key):
    dekey=[]
    
    #其中第一第四列要做2**16+1的乘法逆元，第二三列要被2**16减去，其他直接映射
    tab=[49,50,51,52,47,48,
         43,45,44,46,41,42,
         37,39,38,40,35,36,
         31,33,32,34,29,30,
         25,27,26,28,23,24,
         19,21,20,22,17,18,
         13,15,14,16,11,12,
         7 ,9 ,8 ,10,5 ,6,
         1 ,2 ,3 ,4]
    #由于key中是0~51，所以，tab的取值最后要-1，来配对。
    
    for i in range(52):
        if i%3==0:
            dekey.append(Inverse(key[tab[i]-1],2**16+1))
        elif i%6==1 or i%6==2:
            dekey.append(2**16-key[tab[i]-1])
        else:
            dekey.append(key[tab[i]-1])
            
    return dekey
       

def IDEA_DE(m,k):
    # 密钥转换
    key=to_dekey(get_long_key(k))
    
    # 数据转换
    W=str_16num(six_to_str(m))
    
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
    
    
    #转换成16进制字符串
    result=""
    for i in Y:
        i=str(hex(i)).replace('0x','')
        while(len(i)<4):
            i = '0' + i
        result = result + i
        
    #转换成ASCII字符串再返回
    return six_to_str(result)

# print(IDEA_DE('ce3991ac273d848a','abcdefghijklmnop'))
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑IDEA_De代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''
#处理过长的Data，切片
def to_IDEA_64(msg):
    new_msg=[]
    #16进制编码，一个4位，所以128的判断，就是长度16的16进制字符串判断
    while(len(msg)):
        new_msg.append(msg[:16])
        msg=msg[16:] 
    return new_msg
    
def IDEA_MSG(msg,key):
    new_msg=""
    msg=to_IDEA_64(msg)
    for i in msg:
        new_msg = new_msg+IDEA_DE(i,key)
        
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
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓RSA读取签名代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
#对MD5 即HASH值读取签名，使用公钥
def en_code_RSA(m):
    k=[7, 187]
    c=""
    #由于签名的时候是两个16进制数存一个，所以，读取的时候也要两个一读
    for i in range(0,len(m),2):
        i=int(m[i:i+2],16)
        
        i=(i**k[0])%k[1] #对每个16进制数读取签名
         
        c = c+hex(i)[2:]
    
    return c

#对MD5 即HASH值读取签名，使用公钥
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑RSA读取签名代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''


'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓密钥协商代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
def get_DH_KEY(socket_client):
    p=97
    a=5
    key=""
    while(len(key)<16):
        Xb=(int(time.time())%15)*int(random.random()*100)
        Ya = socket_client.recv(1024).decode('utf-8')
        socket_client.send(str(a**Xb).encode('utf-8'))
        Ya = eval(Ya)
        K_temp=(Ya**Xb)%p
        key = key + chr(K_temp)
    return key

'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑密钥协商代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''

'''
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓RSA解密K代码区↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
def de_RAS(m):
    k=[23, 187]
    c=""
    for i in m:
        i=ord(i)
        i=(i**k[0])%k[1] 
        c = c+chr(i)
    
    return c

'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑RSA解密K代码区↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
'''


#负责接受client的数据，用于解密
def recv(socket_client,key):
    while True:
        
        print("-"*50)
        receive_data = socket_client.recv(4096).decode('utf-8')
        c_key=de_RAS(receive_data[-16:])
        receive_data=receive_data[:-16]
        print("回话使用的密钥为："+c_key)
        
        print("收到一条新信息：  ",end="")
        receive_data=IDEA_MSG(receive_data,key).rstrip() #去除右边填充的空格
        if(operator.eq(en_code_RSA(receive_data[-64:]),MD5(get_code(receive_data[:-64])))):
            print(receive_data[:-64])
        else:
            print("不是那个人发的消息！MD5不等！")

def server():
    host = ("localhost",9897)
    socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_server.bind(host)
    socket_server.listen(5)
    
    while True:
        socket_client,addr = socket_server.accept()
        print("="*50)
        print("HOST:" +str(addr)+"已连接")
        key=get_DH_KEY(socket_client)
        new_t = threading.Thread(target=recv,args=(socket_client,key,))
        new_t.start()
        

server()
