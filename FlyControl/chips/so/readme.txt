;;;
基于MPU9255采集到的九轴姿态原始数据(gyro,acc,mag)计算飞机的欧拉角

python调用c函数，计算过程：
传入九轴原始数据—>计算四元数—>转换成欧拉角

GCC编译命令：
gcc test_a.c test_b.c test_c.c -fPIC -shared -o libtest.so

参考资料：
python调用C动态链接库
https://www.cnblogs.com/lovephysics/p/7237227.html （解决ctype不能输入输出float类型问题）
https://blog.csdn.net/joeblackzqq/article/details/10441017 (返回一个对象/结构体)
;;;


