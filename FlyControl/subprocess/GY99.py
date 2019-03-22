#!/usr/bin/python3
# coding=utf-8
'''
    GY-99传感器，获取以下数据并同步到_1553b_data总线：
    1）欧拉角 Roll  Pitch  Yaw
    2）角速度GYRO X  Y  Z
    3）温度
    4）气压
    5）海拔高度
'''
import serial
import time
from FlyControl.param import config

# 输出数据设置指令,0xFF=输出全部参数
cmd1 = b'\xA5\x55\xFF\xF9'
# 自动输出数据指令
cmd2 = b'\xA5\x56\x02\xFD'
# 波特率设置指=115200
cmd3 = b'\xA5\x58\x01\xFE'
# 设置刷新频率=10HZ
cmd4 = b'\xA5\x59\x01\xFF'
# 加速度陀螺仪校准指令
cmd5 = b'\xA5\x57\x01\xFD'
# 磁力计校准指令 (需人工操作，故不可轻易使用)
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

            while True:
                sr.flushInput()
                while True:
                    n = sr.inWaiting()
                    if n == 46:
                        rec = sr.read(n)
                        __resolve_data(rec,_1553b)
                        break
                    elif n > 46:
                        break
    except Exception as e:
        print(e)
        print("[GY-99]通过串口[%s]获取飞控数据时发生异常..."% config.SERIAL_PORT_GY99)
    finally:
        sr.close()

# 最高位是符号位，最高为位1是负数， 为0是正数
def __hex2dec(hexData):
    if hexData & 0x8000 == 0x8000:
        hexData = hexData ^ 0xFFFF   #异或，相同为0，不同为1
        hexData = ~hexData   #~符号表示运算：~hexData = -(hexData+1)
    return hexData


#处理数据并写入_1553b数据总线
def __resolve_data(data,_1553b):
    if data[:4] == b'\x5A\x5A\xFF\x29':
        #获取陀螺仪 (角度/秒)  >>为什么除以16.4? 看http://www.openedv.com/forum.php?mod=viewthread&tid=80200&page=1
        GYRO_X = (__hex2dec((data[10]<< 8) | data[11])) / 16.4
        _1553b['GYRO_X'] = round(GYRO_X,2)
        GYRO_Y = (__hex2dec((data[12] << 16) | data[13])) / 16.4
        _1553b['GYRO_Y'] = round(GYRO_Y,2)
        GYRO_Z = (__hex2dec((data[14] << 8) | data[15])) / 16.4
        _1553b['GYRO_Z'] = round(GYRO_Z,2)

        #获取欧拉角 (度)
        ROLL = (__hex2dec((data[30]<< 8) | data[31])) / 100
        _1553b['ROLL'] = ROLL
        PITCH = (__hex2dec((data[32] << 16) | data[33])) / 100
        _1553b['PITCH'] = PITCH
        YAW = (__hex2dec((data[34] << 8) | data[35])) / 100
        _1553b['YAW'] = YAW

        #获取气压(KPa)
        Pressure = ((data[36] << 24) | (data[37] << 16) | (data[38] << 8) | data[39]) / 100 / 1000
        _1553b['Pressure'] = round(Pressure,3)

        #获取温度(摄氏度)
        Temp = ((data[40] << 8) | data[41]) / 100
        _1553b['Temp'] = round(Temp,1)

        #获取海拔(米)
        Altitude = ((data[42] << 8) | data[43]) / 100
        _1553b['Altitude'] = round(Altitude,2)

        #已校准
        _1553b['Calibrated'] = data[44]

        print(_1553b)