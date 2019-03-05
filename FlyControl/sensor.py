#!/usr/bin/python3
# coding=utf-8
from FlyControl.subprocess import sim7600
from FlyControl.subprocess import GY99
import threading

def start(_1553b_data):
    try:
        t = threading.Thread(target=GY99.working(), args=(_1553b_data))
        t.setDaemon(True)
        t.start()
    except Exception as e:
        print(e)
    finally:
        pass