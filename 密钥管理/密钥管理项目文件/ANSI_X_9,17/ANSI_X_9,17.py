import Crypto.Cipher.DES3
import binascii
import time
k='8003117156lsh' #长度13的密钥

def fill_key(x):
    if len(x) > 24:
        #196的密钥
        raise "不能超过196"
    else:
        #128的密钥
        while len(x) < 16:
            x += " "
        return x.encode()
 
def des3_en(key,content):
    x = Crypto.Cipher.DES3.new(fill_key(key), Crypto.Cipher.DES3.MODE_ECB)
    #设置加密模式
    en = binascii.b2a_hex(x.encrypt(fill_key(content)))
    #返回16进制字符串
    return en
    
def des3_de(key,content):
    x = Crypto.Cipher.DES3.new(fill_key(key), Crypto.Cipher.DES3.MODE_ECB)
    #设置解密模式
    de = x.decrypt(binascii.a2b_hex(a))
    #处理16进制字符串
    return de

def ANSI(v):
    stock = time.time()
    stock = ((int)(stock*(10**8)))%(2**64)
    #获取时间戳，并截取时间戳的后64位，以便和之后计算的长度匹配。
    #这是第一步
    
    stock=des3_en(k,str(hex(stock)).replace('0x',''))
    stock=stock[:16]
    #对时间戳进行DES3加密，这是第二步
    
    m=int(stock,16)^int(v,16)
    #用内部状态码和时间戳进行XOR运算，这是第三步
    
    m=des3_en(k,str(hex(m)).replace('0x',''))
    m=m[:16]
    #将内部状态码和时间戳的XOR运算的结果进行DES3加密，这是第四步
    
    print(m)
    #输出第四步的结果，即一个伪随机数列
    
    m=int(m,16)^int(stock,16)
    #将加密好的第四步的结果，再与时间戳进行XOR运算，这是第五步
    
    m=des3_en(k,str(hex(m)).replace('0x',''))
    m=m[:16]
    #再将第五步的结果进行DES3加密
    
    return m
    #将重新设置好的状态码返回
    
def main():
    ini_v='abc1234567890abc'
    v=ini_v
    while(True):
        v=ANSI(v)

if __name__=='__main__':
    main()