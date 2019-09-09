#!/usr/bin/python3
# coding=utf-8
'''
开机后，引擎自动初始化，开启四个线程控制分别每个马达
另起一个马达控制线程专门接收飞控数据计算每个马达的PWM
马达线程读取马达控制线程计算出来的PWM执行。

'''
from FlyControl.subprocess import Motor
import threading

def init(_1553b,_1553a,lock):
    thread_list = []
    try:
        t0 = threading.Thread(target=Motor.controller, args=(_1553b,_1553a,lock,))
        #t1 = threading.Thread(target=Motor.working, args=())
        thread_list.append(t0)
        #thread_list.append(t1)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("四轴动力系统进程结束!")