def main():
    print ("1、选择仿射加密 {y=ax+b，a=7，b=21}")
    print ("2、选择仿射解密 {x=(y-b)/a，a=7，b=21}")
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
    
    file=open("1.txt","r")
    dd=file.read()
    file.close
    
    m=""
    
    for a in dd: 
        
        m += chr(((ord(a)-32)*7+21)%95)
        
          
    file=open("1.txt","w")
    file.write(m)
    file.close
    
    
def de_code():
    
    file=open("1.txt","r")
    dd=file.read()
    file.close
    
    
    m=""
    
    for a in dd:
       m += chr((ord(a)*68-3)%95+32)
    
    file=open("1.txt","w")
    file.write(m)
    file.close
    


main()

'''
65--->90  [A-Z]
97--->122 [a-z]
'''
