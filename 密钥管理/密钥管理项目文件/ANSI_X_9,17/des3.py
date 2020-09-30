import Crypto.Cipher.DES3
import binascii
 
def fill_key(x):
    if len(x) > 24:
        #196的密钥
        raise "Too long"
    else:
        #128的密钥
        while len(x) < 16:
            x += " "
        return x.encode()
 
def des3_en(key,content):
    x = Crypto.Cipher.DES3.new(fill_key(key), Crypto.Cipher.DES3.MODE_ECB)
    en = binascii.b2a_hex(x.encrypt(fill_key(content)))
    return en
    
def des3_de(key,content):
    x = Crypto.Cipher.DES3.new(fill_key(key), Crypto.Cipher.DES3.MODE_ECB)
    de = x.decrypt(binascii.a2b_hex(a))
    return de
    
key = "asd"
content = "abcdefg"
print(des3_en(key,content))

