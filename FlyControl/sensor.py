#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import Control_Link
from FlyControl.subprocess import Data_Link
import threading

def start(_1553b_data,_1553b_cmd):
    try:
        t = threading.Thread(target=Control_Link.working(), args=(_1553b_cmd))
        t.setDaemon(True)
        t.start()

        t = threading.Thread(target=Data_Link.working(), args=(_1553b_data))
        t.setDaemon(True)
        t.start()
    except Exception as e:
        print(e)
    finally:
        pass