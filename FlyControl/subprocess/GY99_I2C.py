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
import time
from FlyControl.param import config as cfg

MPU9255 = 0x68

# 根据十六进制数转化为带符号的十进制数
# 最高位是符号位，最高为位1是负数， 为0是正数
def __hex2dec(d):
    if d & 0x8000 == 0x8000:
        d = d ^ 0xFFFF   #异或，相同为0，不同为1
        d = ~d   #~符号表示运算：~d = -(d+1)
    return d

def working(_1553b):
    bus = smbus.SMBus(1)

    try:
        if (init_MPU9255(bus)):
            while True:
                acc_x,acc_y,acc_z = getACC(bus)
                gyro_x,gyro_y,gyro_z = getGYRO(bus)
                print(round(acc_x,2),round(acc_y,2),round(acc_z,2), round(gyro_x,2),round(gyro_y,2),round(gyro_z,2) )
                time.sleep(0.2)
    except Exception as e:
        print(e)

#初始化MPU9255芯片
def init_MPU9255(bus):
    SMPLRT_DIV = 0x19
    CONFIG = 0x1a
    GYRO_CONFIG = 0x1b
    ACCEL_CONFIG = 0x1c
    ACCEL_CONFIG2 = 0x1d
    PWR_MGMT_1 = 0x6b
    PWR_MGMT_2 = 0x6c
    I2C_SLV0_CTRL = 0x27

    WHOAMI = bus.read_i2c_block_data(MPU9255, 0x75, 1)
    if WHOAMI[0] == 0x73:
        bus.write_byte_data(MPU9255,PWR_MGMT_1,0x80)  #电源管理,复位MPU9250
        time.sleep(0.5)
        bus.write_byte_data(MPU9255,SMPLRT_DIV,0x00)    #采样频率  典型值为0X07 1000/(1+0)=1000HZ
        bus.write_byte_data(MPU9255,CONFIG,0x06)      #陀螺仪低通滤波器  典型值0x06 5hz
        bus.write_byte_data(MPU9255,GYRO_CONFIG,0x18)    #陀螺仪测量范围 0X18 ±2000 dps
        bus.write_byte_data(MPU9255,ACCEL_CONFIG,0x18)    #加速度计测量范围 0X18 ±16g
        bus.write_byte_data(MPU9255,ACCEL_CONFIG2,0x06)    #加速度计低通滤波器 0x06 5hz
        print("MPU9255初始化完成")
        return True
    return False

#获取加速度值 x,y,z
def getACC(bus):
   acc = bus.read_i2c_block_data(MPU9255, 0x3b, 6)
   acc_x = __hex2dec((acc[0] << 8) | acc[1]) / 2048  #除以2048 https://blog.csdn.net/u013636775/article/details/69668860
   acc_y = __hex2dec((acc[2] << 8) | acc[3]) / 2048
   acc_z = __hex2dec((acc[4] << 8) | acc[5]) / 2048

   return acc_x,acc_y,acc_z

#获取陀螺仪值 x,y,z
def getGYRO(bus):
    gyro = bus.read_i2c_block_data(MPU9255, 0x43, 6)
    gyro_x = __hex2dec((gyro[0] << 8) | gyro[1]) / 16.4
    gyro_y = __hex2dec((gyro[2] << 8) | gyro[3]) / 16.4
    gyro_z = __hex2dec((gyro[4] << 8) | gyro[5]) / 16.4

    return gyro_x, gyro_y, gyro_z

if __name__ == '__main__':
    working(None)