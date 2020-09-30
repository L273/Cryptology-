def menu():
    li = {
        1:en_file,
        2:de_file
    }
    choose=True
    while(choose):
        try:
            print("1、加密文件")
            print("2、解密文件")
            choose = eval(input("请输入选择："))
            if(choose==2 or choose ==1):
                break
            choose=True

        except:
            choose=True
    
    switch = li.get(choose)
    switch()

def en_file():
    print("将要加密文件")
    m=get_code('1.txt')
    
    if len(m)==0 or len(m)==1:
        print("字符串太短，不足以进行操作。")
        return ;
    
    m=en_code(m)
    
    m=to_str(m)
    
    print("加密后的字符串为："+m)
    
    set_code('1.txt',m)
    
def de_file():
    print("将要解密文件")
    m=get_code('1.txt')
    
    if len(m)==0 or len(m)==1:
        print("字符串太短，不足以进行操作。")
        return ;
    
    m=de_code(m)
    
    m=to_str(m)
    
    print("解密后的字符串为："+m)
    
    set_code('1.txt',m)

def get_code(text):
    print(text)
    fp=open(text,'r')
    dd=fp.read()
    fp.close()
    
    print("\n得到要操作的字符串（非字母均会过滤掉）")
    
    m=[]
    
    print("\n文件内的字符串为：",end="")
    for a in dd:
        if ord(a)<91 and ord(a)>64:
            print(a,end="")
            temp = ord(a)-64+26
        elif ord(a)<123 and ord(a)>96:
            print(a,end="")
            temp = ord(a)-96
        else:
            continue
        m.append(temp)
    '''
    a-z     1->26
    A-Z     27->52
    '''
    print("\n")
    return m

def set_code(text,connect):
    print("\n将把操作的数据写入文件")
    print(text)
    
    try:        
        fp=open(text,'w')
        dd=fp.write(connect)
        fp.close() 
        print("\n写入成功！")
    except:
        print("\n写入失败。")
    
def mul_2(a,b):
    c=[[]for i in range(2)]
    try:
        c[0].append((a[0][0]*b[0][0]+a[0][1]*b[1][0])%52)
    except:
        pass    
    try:
        c[0].append((a[0][0]*b[0][1]+a[0][1]*b[1][1])%52)
    except:
        pass
    try:
        c[1].append((a[1][0]*b[0][0]+a[1][1]*b[1][0])%52)
    except:
        pass
    try:
        c[1].append((a[1][0]*b[0][1]+a[1][1]*b[1][1])%52)
    except:
        pass    
    return c

def mul_3(a,b):
    c=[[]for i in range(3)]
    try:
        c[0].append((a[0][0]*b[0][0]+a[0][1]*b[1][0]+a[0][2]*b[2][0])%52)
    except:
        pass
    try:
        c[0].append((a[0][0]*b[0][1]+a[0][1]*b[1][1]+a[0][2]*b[2][1])%52)
    except:
        pass
    try:
        c[0].append((a[0][0]*b[0][2]+a[0][1]*b[1][2]+a[0][2]*b[2][2])%52)
    except:
        pass
    try:
        c[1].append((a[1][0]*b[0][0] +a[1][1]*b[1][0] +a[1][2]*b[2][0])%52)
    except:
        pass
    try:
        c[1].append((a[1][0]*b[0][1] +a[1][1]*b[1][1] +a[1][2]*b[2][1])%52)
    except:
        pass
    try:
        c[1].append((a[1][0]*b[0][2] +a[1][1]*b[1][2] +a[1][2]*b[2][2])%52)
    except:
        pass
    try:
        c[2].append((a[2][0]*b[0][0]+a[2][1]*b[1][0]+a[2][2]*b[2][0])%52)
    except:
        pass
    try:
        c[2].append((a[2][0]*b[0][1]+a[2][1]*b[1][1]+a[2][2]*b[2][1])%52)
    except:
        pass
    try:
        c[2].append((a[2][0]*b[0][2]+a[2][1]*b[1][2]+a[2][2]*b[2][2])%52)
    except:
        pass
    return c

def en_code(m):
    k2_en=[[51, 13], [43, 20]]
    k3_en=[[22, 30, 19], [23, 41, 6], [2, 35, 10]]
    if(len(m)%5==0):
        c=[[]for i in range((int)(len(m)/5))]
        for i in range(len(c)):
            c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[0][0])
            c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[1][0])
            c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
            c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
            c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        #2323.....23 2323
    elif(len(m)%5==4):
        c=[[]for i in range((int)(len(m)/5)+2)]
        try:
            for i in range(len(c)-2):
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
            
            
        c[-2].append(mul_2(k2_en,[[m[-4]],[m[-3]]])[0][0])
        c[-2].append(mul_2(k2_en,[[m[-4]],[m[-3]]])[1][0])
        
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 2322
    elif(len(m)%5==3):
        c=[[]for i in range((int)(len(m)/5)+1)]
        try:
            for i in range(len(c)-1):
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
            
        except:
            pass
        c[-1].append(mul_3(k3_en,[[m[-3]],[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_3(k3_en,[[m[-3]],[m[-2]],[m[-1]]])[1][0])
        c[-1].append(mul_3(k3_en,[[m[-3]],[m[-2]],[m[-1]]])[2][0])
        
        #2323.....23 233
    elif(len(m)%5==2):
        c=[[]for i in range((int)(len(m)/5)+1)]
        try:
            for i in range(len(c)-1):
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 232
    elif(len(m)%5==1):
        c=[[]for i in range((int)(len(m)/5)+2)]
        try:
            for i in range(len(c)-3):
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_en,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_en,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
        
        
        c[-3].append(mul_2(k2_en,[[m[-6]],[m[-5]]])[0][0])
        c[-3].append(mul_2(k2_en,[[m[-6]],[m[-5]]])[1][0])
    
    
        c[-2].append(mul_2(k2_en,[[m[-4]],[m[-3]]])[0][0])
        c[-2].append(mul_2(k2_en,[[m[-4]],[m[-3]]])[1][0])
        
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_en,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 222
        
    return c

def de_code(m):
    
    k2_de=[[12, 39], [21, 15]]
    k3_de=[[44, 1, 25], [42,26, 45], [47, 18, 4]]

    if(len(m)%5==0):
        c=[[]for i in range((int)(len(m)/5))]
        for i in range(len(c)):
            c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[0][0])
            c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[1][0])
            c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
            c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
            c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        #2323.....23 2323
    elif(len(m)%5==4):
        c=[[]for i in range((int)(len(m)/5)+2)]
        try:
            for i in range(len(c)-2):
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
            
            
        c[-2].append(mul_2(k2_de,[[m[-4]],[m[-3]]])[0][0])
        c[-2].append(mul_2(k2_de,[[m[-4]],[m[-3]]])[1][0])
        
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 2322
    elif(len(m)%5==3):
        c=[[]for i in range((int)(len(m)/5)+1)]
        try:
            for i in range(len(c)-1):
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
            
        except:
            pass
        c[-1].append(mul_3(k3_de,[[m[-3]],[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_3(k3_de,[[m[-3]],[m[-2]],[m[-1]]])[1][0])
        c[-1].append(mul_3(k3_de,[[m[-3]],[m[-2]],[m[-1]]])[2][0])
        
        #2323.....23 233
    elif(len(m)%5==2):
        c=[[]for i in range((int)(len(m)/5)+1)]
        try:
            for i in range(len(c)-1):
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 232
    elif(len(m)%5==1):
        c=[[]for i in range((int)(len(m)/5)+2)]
        try:
            for i in range(len(c)-3):
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[0][0])
                c[i].append(mul_2(k2_de,[[m[5*i]],[m[5*i+1]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[0][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[1][0])
                c[i].append(mul_3(k3_de,[[m[5*i+2]],[m[5*i+3]],[m[5*i+4]]])[2][0])
        except:
            pass
        
        
        c[-3].append(mul_2(k2_de,[[m[-6]],[m[-5]]])[0][0])
        c[-3].append(mul_2(k2_de,[[m[-6]],[m[-5]]])[1][0])
    
    
        c[-2].append(mul_2(k2_de,[[m[-4]],[m[-3]]])[0][0])
        c[-2].append(mul_2(k2_de,[[m[-4]],[m[-3]]])[1][0])
        
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[0][0])
        c[-1].append(mul_2(k2_de,[[m[-2]],[m[-1]]])[1][0])
        
        #2323.....23 222
        
    return c
      
def to_str(list):
    list_str=""
    for i in list:
        for j in i:
            if j<27:
                list_str += chr(j+96)
            elif j<53:
                list_str += chr(j+38)
    
    return list_str
 
def main():
    menu()

if __name__=='__main__':
    main()
    
'''
#a-z     1->26
#A-Z     27->52
'''