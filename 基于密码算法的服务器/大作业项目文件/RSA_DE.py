def de_RAS(m):
    k=[23, 187]
    c=""
    for i in m:
        i=ord(i)
        
        i=(i**k[0])%k[1] 
         
        c = c+chr(i)
    
    return c

print(de_RAS("\°Tw³J"))