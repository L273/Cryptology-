def en_code_RSA(m):
    k=[7, 187]
    c=""
    #由于签名的时候是两个16进制数存一个，所以，读取的时候也要两个一读
    for i in range(0,len(m),2):
        i=int(m[i:i+2],16)
        
        i=(i**k[0])%k[1] #对每个16进制数读取签名
         
        c = c+hex(i)[2:]
    
    return c


print(en_code_RSA('af58b18c9f2a'))