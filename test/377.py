cmd0= "5A 5A"
s = bytes.fromhex(cmd0)
print(s)
print(b'\x5A\x5A\xF0\x02\xFD')

dec = int(input("输入数字:"))
print(dec)
print(bin(dec))
print(oct(dec))
print(hex(dec))
print(type(dec) is oct)
print(b'abcd')
print('中过'.encode("GBK"))

for i in b'\xd6\xd0\xb9\xfd':
    print(i)
    print(bin(i))

print('中C'.encode("utf-8"))


i = 0x06
j= 0x65
print(type(j))
print(((i<<8)|j)/100)

print(65302)