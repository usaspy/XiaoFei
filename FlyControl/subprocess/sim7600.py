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

# 输出数据设置指令,0xFO=输出后四位参数
cmd1 = 'AT+CGPS=1'
# 自动输出数据指令
cmd2 = 'AT+CGPSINFO=1'

def working(_1553b):
    try:
        sr = serial.Serial(port=config.SERIAL_PORT_GPS, baudrate=115200, timeout=15, bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, stopbits=1)

        if sr.isOpen():
            print("串口%s已经打开"% config.SERIAL_PORT_GPS)
            #首先打开GPS，并设置每秒输出一次GPS定位数据
            sr.write(cmd1)
            time.sleep(0.2)
            sr.write(cmd2)
            time.sleep(0.2)

            while True:
                sr.flushInput()
                while True:
                    n = sr.inWaiting()
                    if n > 0:
                        rec = sr.read(n)
                        __resolve_data(rec,_1553b)
                        break
    except Exception as e:
        print("[SIM7600]通过串口[%s]获取GPS数据时发生异常..."% config.SERIAL_PORT_GPS)
    finally:
        sr.close()

#处理数据并写入_1553b数据总线
def __resolve_data(data,_1553b):
    if data.find("+CGPSINFO") == 0:
        data1 = data[data.find(":"):]
        datas = data1.split(",")
        #获取纬度
        LAT = datas[0] + "'" + datas[1]
        _1553b['LAT'] = LAT
        #获取经度
        LOG = datas[2] + "'" + datas[3]
        _1553b['LOG'] = LOG
        #获取海拔高度
        ALT = datas[6]
        _1553b['ALT'] = ALT
        #获取速度
        SPEED = datas[7]
        _1553b['SPEED'] = SPEED