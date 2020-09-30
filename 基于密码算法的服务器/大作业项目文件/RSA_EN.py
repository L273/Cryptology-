def en_RSA(key):
    k=[7, 187]
    c_key=""
    for i in key:
        i=ord(i)
        
        i=(i**k[0])%k[1] #对每个ASCII数值进行加密
        
        c_key = c_key + chr(i)
    return c_key

print(en_RSA('abcdefght'))