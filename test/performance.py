import timeit
s=1
def get_curr_power(No):
    global  s
    if No == 1:
            s='2'
    if No == 2:
            s='2'
    if No == 3:
            s='2'
    if No == 4:
            s='2'
    return None

s = [1,2,3,4]
def get_curr_power2(No):
    for i in s:
        if i == No:
            pass
    return None
z = {1:{1:'0'},2:'aa',3:'4aa',4:{1:'0'}}
def get_curr_power3(No):
    if z[1][1] == No:
        z[1][1]='213aaf'
    return None

def test1():
    get_curr_power(2)
def test2():
    get_curr_power2(2)
def test3():
    get_curr_power3('0')


t1 = timeit.Timer("test1()", "from __main__ import test1")#程序运行时test.py此文件是main
t2 = timeit.Timer("test2()", "from __main__ import test2")#程序运行时test.py此文件是main
t3 = timeit.Timer("test3()", "from __main__ import test3")#程序运行时test.py此文件是main

print("if== ",t1.timeit(number=10000), "seconds")
print("list== ",t2.timeit(number=10000), "seconds")
print("dict== ",t3.timeit(number=10000), "seconds")

print("-----------")
print(z[1][1])
z[1][1]='222'
print(z[1][1])
for i,j in z:
    print(j)
