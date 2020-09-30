#一个Shamir(3,5)的门限方案

#t=3(阈值),n=5(总数)

#p=19(Shamir需要的参数),k=11(Shamir需要的参数),x(1<x<5)

#取a1=2,a2=7构造fx=11+2x+7x2 mod 19

p=19
k=11

from scipy.interpolate import lagrange

def fx(x):
    return (k+2*x+7*(x**2))%19

def get_n():
    key=[]
    for i in range(5):
        key.append([i+1,fx(i+1)])
    return key
    
print(get_n())

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

def lag_3(t1,t2,t3):
    #适用三个值的拉格朗日
    #由于只要计算尾缀的K，所以前面x的系数都不做考虑
    temp1=(t1[1]*((-t2[0])*(-t3[0]))*Inverse(abs((t1[0]-t2[0])*(t1[0]-t3[0])),19))%19
    if (t1[0]-t2[0])*(t1[0]-t3[0])<0:
        temp1=temp1*(p-1)
    temp2=(t2[1]*((-t1[0])*(-t3[0]))*Inverse(abs((t2[0]-t1[0])*(t2[0]-t3[0])),19))%19
    if (t2[0]-t1[0])*(t2[0]-t3[0])<0:
        temp2=temp2*(p-1)
    temp3=(t3[1]*((-t1[0])*(-t2[0]))*Inverse(abs((t3[0]-t1[0])*(t3[0]-t2[0])),19))%19
    if (t3[0]-t1[0])*(t3[0]-t2[0])<0:
        temp3=temp3*(p-1)
        
    result=(int)(temp1+temp2+temp3)%p
    return result
    
'''
def mul(x):
    temp=1
    for i in x:
        temp = (-1)*temp*(i)
    
    return temp
def plus(x):
    temp=0
    for i in x:
        temp = i+temp
    
    return temp


def my_lag(x,y):
    x_high=mul(x)
    x_low=[]
    for i in x:
        for j in x:
            if(i==j):
                continue
            else:
                x_low.append(i-j)
    y_temp=[]
    j=0
    print(x_low)
    for i in y:
        y_temp.append(i*(x_high/x_low[j]))
        j=j+1
    
    result=plus(y_temp)
    
    print(result)
    
    result = result>0 and result or (p-1)*(-1)*(result) 
 
    a=str(result)
    while(a[0]!='.'):
        a=a[1:]
        
    a=int(a.replace('.',''))
   
    result = (int)(result)
    
    result = ((int)(result/p))%p    
'''
#方案排除，有步骤出问题
    
    
def get_k(t1,t2,t3):
    print("\n使用了其中的：")
    print(t1)
    print(t2)
    print(t3)
    #传入三个参数
    x=[]
    y=[]
    x.append(t1[0])
    x.append(t2[0])
    x.append(t3[0])
    y.append(t1[1])
    y.append(t2[1])
    y.append(t3[1])
    print("\n调用Python的库，用于检查：")
    print(lagrange(x,y)[0]%p) 
    #调用函数库，一步解决
    
    #my_lag(x,y) 排除方案
    
    #------------------------------
    #自己写个简单的
    print("\n自己写的简单的：")
    print(lag_3(t1,t2,t3))
    
    #与调用库内饿结果是一致的
    
    
#[[1, 1], [2, 5], [3, 4], [4, 17], [5, 6]]
#由get_n()得到的三个数据
get_k([1, 1], [2, 5], [3, 4])