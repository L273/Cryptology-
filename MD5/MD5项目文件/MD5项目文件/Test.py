import hashlib
data="abcde"
print(hashlib.md5(data.encode(encoding='UTF-8')).hexdigest())