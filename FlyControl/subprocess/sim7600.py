#!/usr/bin/python3
# coding=utf-8
'''
    SIM7600模块，获取以下数据并同步到_1553b_data总线：
    1）GPS坐标
    2）GPRS拨号连接互联网，并实时监控链接状态
'''
import serial
import time
from FlyControl.param import config

def working(_1553b):
    pass