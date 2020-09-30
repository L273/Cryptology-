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

'''
p=23
q=47
e=89
'''
p=11
q=17
e=7
#将映射控制在128到255之间，不会导致过长不易编码，也不会太短放不下ASCII表


p_q=(p-1)*(q-1)
print(p_q)
d=Inverse(e,p_q)
RSA_private=[d,p*q]
RSA_public=[e,p*q]

print("RSA密钥：")
print("私钥：",end='')
print(RSA_private)
print("公钥：",end='')
print(RSA_public)

