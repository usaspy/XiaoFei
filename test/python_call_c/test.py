import ctypes  
ll = ctypes.cdll.LoadLibrary   
lib = ll("./libtest.so")    
lib.test_a()  
s = lib.foo(10,15)
print(s)

#--------------------------------------------
a = ctypes.c_float(13.1)
b = ctypes.c_float(6.6)

foo_float = lib.foo_float
foo_float.restype = ctypes.c_float

z = lib.foo_float(a,b)
print(z)

#--------------------------------------------
class StructPointer(ctypes.Structure):
	_fields_ = [("name", ctypes.c_char * 20), ("age", ctypes.c_int)]

lib.test.restype = ctypes.POINTER(StructPointer)
p = lib.test()
print(p.contents.name,p.contents.age)
