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
        

def IDEA(m,k):
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

print(IDEA("abcdefgh",'abcdefghijklmnop'))       