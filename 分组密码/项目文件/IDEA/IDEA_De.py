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
    
    #其中第一第四列要做2**16+1的乘法逆元，其他的都被2**16减去
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
       
def IDEA(m,k):
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

print(IDEA('ce3991ac273d848a','abcdefghijklmnop'))

