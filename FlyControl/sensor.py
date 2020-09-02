#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import sim7600
from FlyControl.subprocess import GY99
import threading


def start(_1553b):
    thread_list = []
    try:
        t1 = threading.Thread(target=GY99.working, args=(_1553b,))
        #t2 = threading.Thread(target=sim7600.working, args=(_1553b,))
        thread_list.append(t1)
        #thread_list.append(t2)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()
    except Exception as e:
        print(e)
    finally:
        print("传感器数据采集进程停止...")