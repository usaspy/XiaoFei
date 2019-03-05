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

def working(_1553b):
    try:
        sr = serial.Serial(port=config.SERIAL_PORT_GY99, baudrate=115200, timeout=15, bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, stopbits=1)

        if sr.isOpen():
            print("串口%s已经打开"% config.SERIAL_PORT_GY99)
            #首先输出设置
            sr.write(cmd1)
            time.sleep(0.2)
            sr.write(cmd2)
            time.sleep(0.2)
            sr.write(cmd3)
            time.sleep(0.2)
            sr.write(cmd4)
            time.sleep(0.2)
            sr.write(cmd5)
            time.sleep(0.2)
            sr.write(cmd6)
            time.sleep(0.2)
            sr.write(cmd7)
            time.sleep(0.5)

            while True:
                sr.flushInput()
                while True:
                    n = sr.inWaiting()
                    if n == 20:
                        rec = sr.read(n)
                        __resolve_data(rec,_1553b)
                        break
    except Exception as e:
        print(e)
        print("[GY-99]通过串口[%s]获取飞控数据时发生异常..."% config.SERIAL_PORT_GY99)
    finally:
        sr.close()

#处理数据并写入_1553b数据总线
def __resolve_data(data,_1553b):
    if data[:4] == b'\x5A\x5A\xF0\x0F':
        #获取欧拉角 (度)
        ROLL = ((data[4]<< 8) | data[5]) / 100
        _1553b['ROLL'] = ROLL
        PITCH = ((data[6] << 16) | data[7]) / 100
        _1553b['PITCH'] = PITCH
        YAW = ((data[8] << 8) | data[9]) / 100
        _1553b['YAW'] = YAW

        #获取气压(kpa)
        Pressure = ((data[10] << 24) | (data[11] << 16) | (data[12] << 8) | data[13]) / 100 / 1000
        _1553b['Pressure'] = Pressure

        #获取温度(摄氏度)
        Temp = ((data[14] << 8) | data[15]) / 100
        _1553b['Temp'] = Temp

        #获取海拔(米)
        Altitude = ((data[16] << 8) | data[17]) / 100
        _1553b['Altitude'] = Altitude

        #已校准
        Calibrated='no'
        if data[18] == b'\x3F':
            Calibrated='yes'
        _1553b['Calibrated'] = Calibrated