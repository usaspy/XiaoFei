#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import Control_Link
from FlyControl.subprocess import Data_Link
import threading
import time

def start(_1553b,_1553a):
    try:
        t = threading.Thread(target=Control_Link.working, args=(_1553a,))
        t.setDaemon(True)
        t.start()

        t = threading.Thread(target=Data_Link.working, args=(_1553b,))
        t.setDaemon(True)
        t.start()

        while True:
            time.sleep(10)
    except Exception as e:
        print(e)
    finally:
        print("通信进程结束!")