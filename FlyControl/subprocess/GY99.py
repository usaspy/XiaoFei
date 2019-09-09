#!/usr/bin/python3
# coding=utf-8
'''
    GY-99传感器，通过串口方式获取以下数据并同步到_1553b_data总线：
    1）欧拉角 Roll  Pitch  Yaw
    2）角速度GYRO X  Y  Z

    经测试，最高只能设为50HZ,再大接收数据会卡顿，MPU解算不过来
'''
import serial
import time
import datetime
from FlyControl.param import config as cfg

# 输出数据设置指令,0x12=输出部分数据  欧拉角、GYRO角速度
cmd1 = b'\xA5\x55\x12\x0C'
# 自动输出数据指令
cmd2 = b'\xA5\x56\x02\xFD'
# 波特率设置指=115200
cmd3 = b'\xA5\x58\x01\xFE'
# 设置刷新频率=200HZ
cmd4 = b'\xA5\x59\x04\x02'
# 加速度陀螺仪校准指令
cmd5 = b'\xA5\x57\x01\xFD'
# 磁力计校准指令 (需人工操作，故不可轻易使用)
cmd6 = b'\xA5\x57\x02\xFE'
# 保存设置
cmd7 = b'\xA5\x5A\x01\x00'
# 恢复出厂设置
cmd8 = b'\xA5\x5A\x02\x01'

def working(_1553b,lock):
    try:
        sr = serial.Serial(port=cfg.SERIAL_PORT_GY99, baudrate=115200, timeout=15, bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, stopbits=1)

        if sr.isOpen():
            print("串口%s已经打开"% cfg.SERIAL_PORT_GY99)
            #首先输出设置
            sr.write(cmd1)
            time.sleep(0.5)
            sr.write(cmd2)
            time.sleep(0.5)
            sr.write(cmd3)
            time.sleep(0.5)
            sr.write(cmd4)
            time.sleep(0.5)
            #sr.write(cmd5) #模块上电后会自动校准，可不用再执行校准程序
            #time.sleep(5) #加陀校准时要保证至少三秒以上静止状态
            ba = bytearray()
            while True:
                n = sr.inWaiting()
                if n > 0:
                    rec = sr.read(n)
                    ba.extend(rec)
                    if ba.__len__() > 18:  # 这是个经验值，理论上该值越小，实时性就越好，不能低于18  必要时可增加一个不能超过的最大值，预防后续程序处理太慢了造成数据积压，影响实时性。
                        try:
                            i = ba.index(b'\x5A\x5A\x12\x0D')
                            data = ba[i:18]
                            del ba[0:18 + i]
                            __resolve_data(data,_1553b,lock)
                            #time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
                            #print(time_now)
                        except Exception:
                            ba.clear()
                            continue
    except Exception as e:
        print(e)
        print("[GY-99]通过串口[%s]获取飞控数据时发生异常..."% cfg.SERIAL_PORT_GY99)
    finally:
        sr.close()

# 根据十六进制数转化为带符号的十进制数
# 最高位是符号位，最高为位1是负数， 为0是正数
def __hex2dec(d):
    if d & 0x8000 == 0x8000:
        d = d ^ 0xFFFF   #异或，相同为0，不同为1
        d = ~d   #~符号表示运算：~d = -(d+1)
    return d


#处理数据并写入_1553b数据总线
def __resolve_data(data,_1553b,lock):
    #获取陀螺仪 (角度/秒) 默认量程2000  >>为什么除以16.4? 看http://www.openedv.com/forum.php?mod=viewthread&tid=80200&page=1
    GYRO_X = (__hex2dec((data[4]<< 8) | data[5])) / 16.4
    GYRO_Y = (__hex2dec((data[6] << 8) | data[7])) / 16.4
    GYRO_Z = (__hex2dec((data[8] << 8) | data[9])) / 16.4

        #获取欧拉角 (度)
    ROLL = (__hex2dec((data[10]<< 8) | data[11])) / 100
    PITCH = (__hex2dec((data[12] << 8) | data[13])) / 100
    YAW = (__hex2dec((data[14] << 8) | data[15])) / 100

    with lock:  # Manager默认是加了锁的，这里再加锁是为了同步更新以下这一批数据
        _1553b['GYRO_X'] = round(GYRO_X,2)
        _1553b['GYRO_Y'] = round(GYRO_Y,2)
        _1553b['GYRO_Z'] = round(GYRO_Z,2)
        _1553b['ROLL'] = ROLL
        _1553b['PITCH'] = PITCH
        _1553b['YAW'] = YAW
        _1553b['Calibrated'] = data[16]   #已校准

    #print(_1553b)