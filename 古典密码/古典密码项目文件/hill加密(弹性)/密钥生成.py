import random
def n2():
    a=[[] for i in range(2)]
    for i in range(4):
        a[i%2].append(random.randint(1,52))
    while not (a[0][0]*a[1][1]-a[0][1]*a[1][0]):
        a=[[] for i in range(2)] 
        for i in range(4):
            a[i%2].append(random.randint(1,52))
        break
    return a

def K_2(k2):
    k2_temp=[[]for i in range(2)]
    re = Inverse((k2[0][0]*k2[1][1]-k2[0][1]*k2[1][0])%52)
    k2_temp[0].append(re*k2[1][1]%52)
    k2_temp[0].append(re*(-k2[0][1])%52)
    k2_temp[1].append(re*(-k2[1][0])%52)
    k2_temp[1].append(re*k2[0][0]%52)
    
    return k2_temp

def n3():
    a=[[] for i in range(3)]
    for i in range(9):
        a[i%3].append(random.randint(1,52))
    while not (a[0][0]*a[1][1]*a[2][2]+a[0][1]*a[1][2]*a[2][0]+a[0][2]*a[1][0]*a[2][1]\
    -a[0][0]*a[1][2]*a[2][1]-a[0][1]*a[1][0]*a[2][2]-a[0][2]*a[1][1]*a[2][0]):
        a=[[] for i in range(3)] 
        for i in range(9):
            a[i%3].append(random.randint(1,52))
        break
    return a

def K_3(k3):
    k3_temp=[[]for i in range(3)]
    re = Inverse((k3[0][0]*k3[1][1]*k3[2][2]+k3[0][1]*k3[1][2]*k3[2][0]+k3[0][2]*k3[1][0]*k3[2][1]\
    -k3[0][0]*k3[1][2]*k3[2][1]-k3[0][1]*k3[1][0]*k3[2][2]-k3[0][2]*k3[1][1]*k3[2][0])%52)

    k3_temp[0].append(re*(k3[1][1]*k3[2][2]-k3[2][1]*k3[1][2])%52)
    k3_temp[0].append(re*(k3[2][1]*k3[0][2]-k3[0][1]*k3[2][2])%52)
    k3_temp[0].append(re*(k3[0][1]*k3[1][2]-k3[0][2]*k3[1][1])%52)
    k3_temp[1].append(re*(k3[1][2]*k3[2][0]-k3[1][0]*k3[2][2])%52)
    k3_temp[1].append(re*(k3[2][2]*k3[0][0]-k3[0][2]*k3[2][0])%52)
    k3_temp[1].append(re*(k3[0][2]*k3[1][0]-k3[1][2]*k3[0][0])%52)
    k3_temp[2].append(re*(k3[1][0]*k3[2][1]-k3[2][0]*k3[1][1])%52)
    k3_temp[2].append(re*(k3[2][0]*k3[0][1]-k3[2][1]*k3[0][0])%52)
    k3_temp[2].append(re*(k3[0][0]*k3[1][1]-k3[1][0]*k3[0][1])%52)
    
    return k3_temp

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

def main():
    k2 = n2()
    k3 = n3()
    
    while not Inverse((k2[0][0]*k2[1][1]-k2[1][0]*k2[0][1])%52):
        k2=n2()
        
    print (k2)
    k2 = K_2(k2)
    print (k2)
    
    
    while not Inverse((k3[0][0]*k3[1][1]*k3[2][2]+k3[0][1]*k3[1][2]*k3[2][0]+k3[0][2]*k3[1][0]*k3[2][1]\
    -k3[0][0]*k3[1][2]*k3[2][1]-k3[0][1]*k3[1][0]*k3[2][2]-k3[0][2]*k3[1][1]*k3[2][0])%52):
        k3=n3()
    
    print (k3)
    k3 = K_3(k3)
    print (k3)
    
main()
    
'''
三阶解密密钥有问题
（Done！）


已解决
原因：随阵的几个角标弄错了。
'''


    
    

    
    
