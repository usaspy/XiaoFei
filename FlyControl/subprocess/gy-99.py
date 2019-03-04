#!/usr/bin/python3
# coding=utf-8
'''
    GY-99传感器，获取以下数据并同步到_1553b_data总线：
    1）欧拉角 Roll  Pitch  Yaw
    2）加速度 X  Y  Z
    3）温度
    4）气压
    5）海拔高度
'''
import serial
import time
from FlyControl.param import config

# 输出数据设置指令,0xFO=输出后四位参数
cmd1 = b'\xA5\x55\xF0\xEA'
# 自动输出数据指令
cmd2 = b'\xA5\x56\x02\xFD'
# 波特率设置指=115200
cmd3 = b'\xA5\x58\x01\xFE'
# 设置刷新频率=10HZ
cmd4 = b'\xA5\x59\x01\xFF'
# 加速度陀螺仪校准指令
cmd5 = b'\xA5\x57\x01\xFD'
# 磁力计校准指令
cmd6 = b'\xA5\x57\x02\xFE'
# 保存设置
cmd7 = b'\xA5\x5A\x01\x00'
# 恢复出厂设置
cmd8 = b'\xA5\x5A\x02\x01'

def working(_1553b_data):
    try:
        sr = serial.Serial(port=config.SERIAL_PORT_GY99, baudrate=115200, timeout=15, bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, stopbits=1)

        if sr.isOpen():
            print("串口%s已经打开"% config.SERIAL_PORT_GY99)
            #首先输出设置
            sr.write(cmd1)
            time.sleep(0.5)
            sr.write(cmd2)
            time.sleep(0.5)
            sr.write(cmd3)
            time.sleep(0.5)
            sr.write(cmd4)
            time.sleep(0.5)
            sr.write(cmd5)
            time.sleep(0.5)
            sr.write(cmd6)
            time.sleep(0.5)
            sr.write(cmd7)
            time.sleep(0.5)

            while True:
                sr.flushInput()
                n = sr.inWaiting()
                if n == 20:
                    rec = sr.read(n)
                    print(rec)
                    __resolve_data(rec,_1553b_data)
                    print(len(rec))
    except Exception as e:
        print(e)
        print("[GY-99]通过串口[%s]获取飞控数据时发生异常..."% config.SERIAL_PORT_GY99)
    finally:
        sr.close()

def __resolve_data(data,_1553b_data):
    data = b'ZZ\xf0\x0f\xda\xbd\xfd\xe7\xdc\xa5\x00\x91\xabR\x08j\xc3-\x0c\xab'
    pass