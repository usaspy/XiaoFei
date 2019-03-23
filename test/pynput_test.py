import timeit
def a():
    i = 0
    b(i)

def b(i):
    i= 1

def z():
    i =2
    i =i+1
    print(i)
if __name__ == '__main__':
    #t1 = timeit.Timer("a()", "from __main__ import a")  # 程序运行时test.py此文件是main
   # print("if== ", t1.timeit(number=1000000), "seconds")
   z()
