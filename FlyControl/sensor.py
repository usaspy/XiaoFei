#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import sim7600
from FlyControl.subprocess import GY99
import threading
import time

def start(_1553b):
    try:
        t = threading.Thread(target=GY99.working, args=(_1553b,))
        t.setDaemon(True)
        t.start()

        t.join()
    except Exception as e:
        print(e)
    finally:
        print("传感器数据采集进程停止...")