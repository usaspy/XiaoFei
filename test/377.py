b = b'\r\n+CGPSINFO: 3039.049728,N,10359.829396,E,090319,141329.0,612.5,0.0,328.9\r\n'
s = b.decode("ascii")
if s.find("\r\n+CGPSINFO:") == 0:
    data = s[s.find(": ")+1:]
    datas = data.split(",")
    print(datas[0].strip())
    # 获取纬度
    LAT = datas[0] + "'" + datas[1]
    # 获取经度
    LOG = datas[2] + "'" + datas[3]
    # 获取海拔高度
    ALT = datas[6]
    # 获取速度
    SPEED = datas[7]

pass
s= "{'ROLL': 653.34, 'PITCH': 167118.53, 'Calibrated': 'no', 'YAW': 562.24, 'p2_status': 0, 'p1_status': 0, 'Pressure': 96.02383, 'Temp': 21.26, 'p3_status': 0, 'Altitude': 451.01}"
d = eval(s)
print(d)
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