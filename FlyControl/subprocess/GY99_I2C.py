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
from FlyControl.chips.MPU9255 import MPU9255
from FlyControl.chips.BMP280 import BMP280x
import time
#from FlyControl.param import config as cfg

MPU9255_ADDR = 0x68
BMP280_ADDR = 0x76

def working(_1553b):
    bus = smbus.SMBus(1)
    count = 0
    try:
        mpu9255 = MPU9255(bus,MPU9255_ADDR)
        BMP280 = BMP280x(bus,BMP280_ADDR)
        while True:
            try:
                acc_x,acc_y,acc_z = mpu9255.getACC()
                gyro_x,gyro_y,gyro_z = mpu9255.getGYRO()
                if count >= 100:  #
                    temp,press = BMP280.getTEMP_PRESS()
                    count = 0
                count = count + 1
                print(round(acc_x,2),round(acc_y,2),round(acc_z,2), round(gyro_x,2),round(gyro_y,2),round(gyro_z,2))
                time.sleep(0.2)
            except Exception as e:
                print("数据读取错误" + e)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    working(None)