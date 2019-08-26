#!/usr/bin/python3
# coding=utf-8
import time

class MPU9255(object):
    SMPLRT_DIV = 0x19
    CONFIG = 0x1a
    GYRO_CONFIG = 0x1b
    ACCEL_CONFIG = 0x1c
    ACCEL_CONFIG2 = 0x1d
    PWR_MGMT_1 = 0x6b
    PWR_MGMT_2 = 0x6c

    # 初始化MPU9255芯片
    def __init__(self,bus,addr):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0x75, 1)
        if WHOAMI[0] == 0x73:
            bus.write_byte_data(self.addr, self.PWR_MGMT_1, 0x80)  # 电源管理,复位MPU9250
            time.sleep(0.5)
            # bus.write_byte_data(MPU9255,PWR_MGMT_1,0x00)  # 电源管理1，解除休眠状态，正常启动
            # time.sleep(0.5)
            # bus.write_byte_data(MPU9255,PWR_MGMT_1,0x03)  # 电源管理1，选时钟
            bus.write_byte_data(self.addr, self.SMPLRT_DIV, 0x00)  # 采样频率  典型值为0X07 1000/(1+0)=1000HZ
            bus.write_byte_data(self.addr, self.GYRO_CONFIG, 0x18)  # 陀螺仪测量范围 0X18 ±2000 dps
            bus.write_byte_data(self.addr, self.ACCEL_CONFIG, 0x00)  # 加速度计测量范围 0X18 ±2g 16384LSB/g
            bus.write_byte_data(self.addr, self.ACCEL_CONFIG2, 0x06)  # 加速度计低通滤波器 0x06 5hz
            bus.write_byte_data(self.addr, self.CONFIG, 0x06)  # 陀螺仪低通滤波器  典型值0x06 5hz
            # bus.write_byte_data(MPU9255,PWR_MGMT_2,0x00)  # 电源管理2　使加速度陀螺仪都工作

            print("MPU9255初始化完成")

    # 根据十六进制数转化为带符号的十进制数
    # 最高位是符号位，最高为位1是负数， 为0是正数
    def __hex2dec(self,d):
        if d & 0x8000 == 0x8000:
            d = d ^ 0xFFFF  # 异或，相同为0，不同为1
            d = ~d  # ~符号表示运算：~d = -(d+1)
        return d

    # 获取加速度值 x,y,z
    def getACC(self):
        acc = self.bus.read_i2c_block_data(self.addr, 0x3b, 6)
        acc_x = self.__hex2dec(
            (acc[0] << 8) | acc[1]) / 16384  # 16384 https://blog.csdn.net/u013636775/article/details/69668860
        acc_y = self.__hex2dec((acc[2] << 8) | acc[3]) / 16384
        acc_z = self.__hex2dec((acc[4] << 8) | acc[5]) / 16384

        return acc_x, acc_y, acc_z

    # 获取陀螺仪值 x,y,z
    def getGYRO(self):
        gyro = self.bus.read_i2c_block_data(self.addr, 0x43, 6)
        gyro_x = self.__hex2dec((gyro[0] << 8) | gyro[1]) / 16.4
        gyro_y = self.__hex2dec((gyro[2] << 8) | gyro[3]) / 16.4
        gyro_z = self.__hex2dec((gyro[4] << 8) | gyro[5]) / 16.4

        return gyro_x, gyro_y, gyro_z