def de_code_RSA(c):
    k=[23, 187]
    m=""
    for i in c:
        i=int(i,16)
        
        i=(i**k[0])%k[1] #对每个16进制数进行签名
        
        m = i>16 and m+hex(i)[2:] or m+'0'+hex(i)[2:]
    return m

print(de_code_RSA([97, 98, 99, 100, 101]))