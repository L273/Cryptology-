from pyDes import des, CBC, PAD_PKCS5
import binascii
def des_encrypt(s,KEY):
    #   加密
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    print(en)
    return binascii.b2a_hex(en)
 
def des_descrypt(s,KEY):
    #   解密
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

def des_three_en(s):
    key1='LiuShihu'
    key2='i1704156'
    s=des_encrypt(s,key1)
    print(s)
    s=des_descrypt(s,key1)
    print(s)
    s=des_encrypt(s,key1)
    print(s)
    return s

#   des_three_en('123')

#   pyDes定义了向量vi，若密钥不对，返回值为0。这个三重不能实现