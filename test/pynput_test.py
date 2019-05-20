import time

cmd = b'\x20\x19\x10\x0e'

s = str([0,0,0,0,0,0]).encode("utf-8")
a = cmd + s
print(a[0:4])
if a[0:3] == b'\x20\x19\x10\x0e':
    print(a[4:])
