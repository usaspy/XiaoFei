#!/usr/bin/python3
# coding=utf-8
'''
    GY-99传感器( MPU9255 + BMP280 )，通过I2C接口获取原始数据，计算出以下数据同步到_1553b_data总线：
    1） 3轴加速度
    2） 3轴陀螺计
    3） 3轴磁力计
    计算出：
    1）欧拉角 Roll  Pitch  Yaw
    2）角速度GYRO X  Y  Z

'''
import smbus
import ctypes
from FlyControl.chips.MPU9255 import MPU9255
from FlyControl.chips.BMP280 import BMP280x
from FlyControl.chips.AK8963 import AK8963x
import time
#from FlyControl.param import config as cfg

MPU9255_ADDR = 0x68
BMP280_ADDR = 0x76
AK8963_ADDR = 0x0c

def working(_1553b):
    bus = smbus.SMBus(1)
    count = 0
    try:
        mpu9255 = MPU9255(bus,MPU9255_ADDR,_1553b)
        BMP280 = BMP280x(bus,BMP280_ADDR)
        AK8963 = AK8963x(bus,AK8963_ADDR)
        while True:
            try:
                acc_x,acc_y,acc_z = mpu9255.getACC()
                gyro_x,gyro_y,gyro_z = mpu9255.getGYRO()
                mag_x,mag_y,mag_z = AK8963.getMAG()
                if count >= 1000:  #
                    temp,press = BMP280.getTEMP_PRESS()   #摄氏度  千帕
                    count = 0
                count = count + 1

                print(round(acc_x,2),round(acc_y,2),round(acc_z,2), round(gyro_x,2),round(gyro_y,2),round(gyro_z,2),mag_x,mag_y,mag_z)
                time.sleep(0.2)

            except Exception as e:
                print("数据读取错误" + e)
    except Exception as e:
        print(e)


#调用九轴融合算法计算欧拉角并写入_1553b数据总线
def __resolve_data(acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,mag_x,mag_y,mag_z,_1553b):
    ll = ctypes.cdll.LoadLibrary
    lib = ll("/home/pi/libAHRS.so")

    class StructPointer(ctypes.Structure):
        _fields_ = [("roll", ctypes.c_float), ("yitch", ctypes.c_float), ("yaw", ctypes.c_float)]

    lib.getAHRS.restype = ctypes.POINTER(StructPointer)

    gx = ctypes.c_float(gyro_x)
    gy = ctypes.c_float(gyro_y)
    gz = ctypes.c_float(gyro_z)

    ax = ctypes.c_float(acc_x)
    ay = ctypes.c_float(acc_y)
    az = ctypes.c_float(acc_z)

    mx = ctypes.c_float(mag_x)
    my = ctypes.c_float(mag_y)
    mz = ctypes.c_float(mag_z)

    dt = ctypes.c_float(0.002)

    p = lib.getAHRS(gx, gy, gz, ax, ay, az, mx, my, mz, dt)

    _1553b['GYRO_X'] = round(gyro_x, 2)
    _1553b['GYRO_Y'] = round(gyro_y, 2)
    _1553b['GYRO_Z'] = round(gyro_z, 2)

    # 获取欧拉角 (度)
    _1553b['ROLL'] = p.contents.roll
    _1553b['PITCH'] = p.contents.yitch
    _1553b['YAW'] = p.contents.yaw

if __name__ == '__main__':
    working(None)