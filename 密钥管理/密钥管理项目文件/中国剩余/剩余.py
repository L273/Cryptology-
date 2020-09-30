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


#   选取一个大素数 p=7 , k=4 
#   m1=9    m2=11   m3=13
#   t=2 n=3

p=7
l=10

#密钥生成
def get_n():
    m=[9,11,13]
    k_n=[]
    k=4
    L=k+l*p
    for i in m:
        k_n.append([i,L%i])
        
    return k_n
    
print(get_n())
#[[9, 2], [11, 8], [13, 9]]  


def chinse(x,y):
    M=1
    for i in x:
        M=M*i
    L=0
    j=0
    for i in x:
        L = L+ (y[j]*(M/i))*Inverse((int)(M/i),i)
        j+=1
    L=(int)(L%M)
    k=L-l*p
    print(k)
 
#选取前两个
chinse([9, 11],[2, 8])