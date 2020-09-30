def main():
    print ("1、选择凯撒加密（K=8）")
    print ("2、选择凯撒解密（K=8) ")
    try:
        choose = eval(input("请输入您的选择："))
    except:
        print("Error：请不要输入选项以外的东西")
    
    if choose==1:
        en_code();
    elif choose==2:
        de_code();
    else:
        print("无法识别您的选择。")

    

def en_code():
    
    dd=input("请输入要加密的字符串：")
    
    m1=[]
    m2=""
    
    for a in dd:
        if ord(a)<91 and ord(a)>64:
            temp = ord(a)-64+26
        elif ord(a)<123 and ord(a)>96:
            temp = ord(a)-96
        else:
            continue
        
        m1.append((temp+8)%52)
    
    for b in m1:
        if b<27:
            m2=m2+chr(b+96)
        else:
            m2=m2+chr(b+64-26)
    print ("加密的密文为:" + m2) 
    
    
    
    
def de_code():
    
    dd=input("请输入要解密的字符串：")
    
    m1=[]
    m2=""
    
    for a in dd:
        if ord(a)<91 and ord(a)>64:
            temp = ord(a)-64+26
        elif ord(a)<123 and ord(a)>96:
            temp = ord(a)-96
        else:
            continue
        
        if temp<8:
            temp += 52
        
        m1.append((temp-8)%52)
    
    for b in m1:
        if b<27:
            m2=m2+chr(b+96)
        else:
            m2=m2+chr(b+64-26)
    print ("解出的明文为:" + m2) 



main()



'''
65--->90  [A-Z]
97--->122 [a-z]
'''