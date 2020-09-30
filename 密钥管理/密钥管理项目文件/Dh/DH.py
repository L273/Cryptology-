def talk():
    p=97
    a=5
    print("\n初始化a=%d,p=%d\n" %(a,p))
    
    Xa=36
    print("A选择了一个Xa=%d\n" %Xa)
    
    Xb=58
    print("B选择了一个Xb=%d\n" %Xb)
    
    Ya=(a**Xa)%p
    print("A计算出Ya=%d\n" %Ya)
    
    Yb=(a**Xb)%p
    print("B计算出Yb=%d\n" %Yb)
    
    K=(Yb**Xa)%p
    print("A拿到Yb,后计算出K(Yb的Xa次幂)mod p=K=%d\n" %K)
    
    K=(Ya**Xb)%p
    print("B拿到Ya,后计算出K(Ya的Xb次幂)mod p=K=%d\n" %K)

talk()