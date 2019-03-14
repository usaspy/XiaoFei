#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import MotorX
import threading
import time
import RPi.GPIO as GPIO

def init(_1553b,_1553a):
    thread_list = []
    try:
        t1 = threading.Thread(target=MotorX.working, args=(_1553a,))
        t2 = threading.Thread(target=MotorX.working, args=(_1553a,))
        t3 = threading.Thread(target=MotorX.working, args=(_1553a,))
        t4 = threading.Thread(target=MotorX.working, args=(_1553a,))
        thread_list.append(t1)
        thread_list.append(t2)
        thread_list.append(t3)
        thread_list.append(t4)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("四轴动力控制系统进程结束!")