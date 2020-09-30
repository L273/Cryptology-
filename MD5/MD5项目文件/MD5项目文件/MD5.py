#这个hash算法，在get_code的时候就已经把一些ASCII字符外的数据过滤了。所以，如果是有其他编码形式的文件，这个MD5算不来

T=[0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
	0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
	0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
	0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
	0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
	0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
	0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
	0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]
    
def get_code(text):
    print(text)
    fp=open(text,'r',encoding='utf-8')
    dd=fp.read()
    fp.close()
    m=[]
    
    print("\n载入要操作的字符串")
    
    for i in dd:
        if(ord(i)<128):
            m.append(ord(i))
        #只接受ASCII码内的值
    print("\n载入完成")
    
    return m
def set_code(text,connect):
    print("\n把该MD5值写入文件：")
    print(text)
    
    try:        
        fp=open(text,'w')
        dd=fp.write(connect)
        fp.close() 
        print("\n写入成功！")
    except:
        print("\n写入失败。")

'''
def section(m):
    # c=[]
    length=len(m)
    if len(m)>=64:
        #大于等于512的情况
       
        long=(int)(len(m)/64)
        for i in range(long):
            temp=0
            for j in range(64):
                temp = temp**8 + m[i*8+j]
            m=m[(i+1)*64:]
            
            c.append(temp)
       
        
    #大片切完,然后对剩余的处理
    if len(m)==63:
        #504的情况,由于我的想法是插入两个值来计算，而这个仅仅只能插入一个值，单独处理
        m.append(0x80)
        
        temp=0
        for j in range(64):
            temp = temp**8 + m[0+j]
        c.append(temp) #补齐512
        
        c.append(0) #末尾填充的448个0
        
    elif len(m)>=56:
        #大于等于448的情况
        m.append(0x80) #插入值
        m.insert(0,0x80) #头限定
        temp=0
        for i in m:
            temp = temp**8+i
        
        while((int)(temp/2**512)!=0):
            temp=temp<<1
        #配合头限定定位，然后再右移8次就OK了。
        for i in range(8):
            temp=temp<<1
        c.append(temp) #补齐512
        
        c.append(0) #末尾填充的48个0
        
    else:
        #小于448的情况
        m.append(0x80)
        temp=0
        for i in m:
            temp = temp**8+i
        c.append(temp)
    
    #填充完毕，然后再加入最后64位的消息长度。
    
    temp=1 #头界定
    while(temp<length):
        temp=temp<<1
    
    temp=temp+length
    
    while((int)(temp/2**64)!=0):
        temp=temp<<1
    temp=temp<<1 #把一开始的temp给移掉
    
    length=temp
    
    c[-1]=(c[-1]*(2**64))+length 
   
    return m
'''
#让处理器爆炸的切片

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
        re_hash = re_hash + str(hex(j)).strip('0x')
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

def main():
    hash = MD5(get_code("Alan Turing.txt"))
    print("\n得到Hash值：")
    print(hash)
    set_code("MD5_hash.txt",hash)

if __name__=='__main__':
    main()
    


'''
如果将数据存为2**512大小的数据，处理器已爆炸，改方案
'''

'''
一个大的出错原因，就是在最后输出的时候，忘记reverse，而直接把小端形式的数据输出，而于test验证的结果出错
'''