#!/usr/bin/python3
# coding=utf-8
import time
'''
从MPU9255模块获取实时的陀螺计、加速度计数据
'''
class MPU9255(object):
    SMPLRT_DIV = 0x19
    CONFIG = 0x1a
    GYRO_CONFIG = 0x1b
    ACCEL_CONFIG = 0x1c
    ACCEL_CONFIG2 = 0x1d
    PWR_MGMT_1 = 0x6b
    PWR_MGMT_2 = 0x6c

    #I2C_SLV0_CTRL = 0x27
    #I2C_SLV0_ADDR = 0x25
    #I2C_SLV0_REG = 0x26
    #USER_CTRL = 0x6a

    INT_PIN_BYPASS = 0x37

    #加速度、角速度的零偏补偿值
    ACC_X_OFFSET = 0
    ACC_Y_OFFSET = 0
    ACC_Z_OFFSET = 0
    GYRO_X_OFFSET = 0
    GYRO_Y_OFFSET = 0
    GYRO_Z_OFFSET = 0

    # 初始化MPU9255芯片
    def __init__(self,bus,addr,_1553b):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0x75, 1)
        if WHOAMI[0] == 0x73:
            bus.write_byte_data(self.addr, self.PWR_MGMT_1, 0x80)  # 电源管理,复位MPU9250
            time.sleep(0.5)
            # bus.write_byte_data(MPU9255,PWR_MGMT_1,0x00)  # 电源管理1，解除休眠状态，正常启动
            # time.sleep(0.5)
            # bus.write_byte_data(MPU9255,PWR_MGMT_1,0x03)  # 电源管理1，选时钟
            bus.write_byte_data(self.addr, self.SMPLRT_DIV, 0x02)  # 采样频率  典型值为0X07 1000/(1+2)=333HZ  频率越高，噪音越大
            bus.write_byte_data(self.addr, self.GYRO_CONFIG, 0x18)  # 陀螺仪测量范围 0X18 ±2000 dps
            bus.write_byte_data(self.addr, self.ACCEL_CONFIG, 0x00)  # 加速度计测量范围 0X18 ±2g 16384LSB/g
            bus.write_byte_data(self.addr, self.ACCEL_CONFIG2, 0x06)  # 加速度计低通滤波器 0x06 5hz    过滤噪音，但频率太高会导致较大延迟
            bus.write_byte_data(self.addr, self.CONFIG, 0x06)  # 陀螺仪低通滤波器  典型值0x06 5hz
            # bus.write_byte_data(MPU9255,PWR_MGMT_2,0x00)  # 电源管理2　使加速度陀螺仪都工作
            time.sleep(0.1)

            # I2C Master方式读取AKM8963模块的地磁数据
            #bus.write_byte_data(self.addr,self.I2C_SLV0_CTRL,0x86)    #  0x80 | 8 启用第一个从机配置,读取6byte数据。10000110=接收6个字节的磁力计数据     https://www.cnblogs.com/leptonation/p/5225889.html
            #bus.write_byte_data(self.addr,self.I2C_SLV0_REG,0x03)    #起始读取位置设置 0x00
            #bus.write_byte_data(self.addr,self.I2C_SLV0_ADDR,0x8c)    #Slave 0 I2C Address    AK8963_I2C_ADDR | 0x80
            #bus.write_byte_data(self.addr,self.USER_CTRL,0x20)    #I2C Master Mode Enable  启用

            # Pass Through Mode，从 Host 用 I2C 总线直接连 AKM8963
            bus.write_byte_data(self.addr, self.INT_PIN_BYPASS, 0x02)  # 设置ByPass从0x0c AKM8963设备读取地磁数据
            time.sleep(0.1)

            #计算加速度计、陀螺计零偏补偿值
            self.do_Calibrating(_1553b)
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
        acc_x = self.__hex2dec((acc[0] << 8) | acc[1]) / 16384  # 16384 https://blog.csdn.net/u013636775/article/details/69668860
        acc_y = self.__hex2dec((acc[2] << 8) | acc[3]) / 16384
        acc_z = self.__hex2dec((acc[4] << 8) | acc[5]) / 16384

        acc_x = acc_x + self.ACC_X_OFFSET
        acc_y = acc_y + self.ACC_Y_OFFSET
        acc_z = acc_z + self.ACC_Z_OFFSET

        return acc_x, acc_y, acc_z

    # 获取陀螺仪值 x,y,z
    def getGYRO(self):
        gyro = self.bus.read_i2c_block_data(self.addr, 0x43, 6)
        gyro_x = self.__hex2dec((gyro[0] << 8) | gyro[1]) / 16.4
        gyro_y = self.__hex2dec((gyro[2] << 8) | gyro[3]) / 16.4
        gyro_z = self.__hex2dec((gyro[4] << 8) | gyro[5]) / 16.4

        gyro_x = gyro_x + self.GYRO_X_OFFSET
        gyro_y = gyro_y + self.GYRO_Y_OFFSET
        gyro_z = gyro_z + self.GYRO_Z_OFFSET

        return gyro_x, gyro_y, gyro_z

    '''
        计算加速度和陀螺的零偏补偿值
        开机初始化时执行一次
        允许前端触发执行校准操作
        需飞机水平静置5秒左右时间
    '''
    def do_Calibrating(self,_1553b):
        _1553b['Calibrated'] = 0x3F #正在校准
        #补偿值清零
        self.ACC_X_OFFSET = 0
        self.ACC_Y_OFFSET = 0
        self.ACC_Z_OFFSET = 0
        self.GYRO_X_OFFSET = 0
        self.GYRO_Y_OFFSET = 0
        self.GYRO_Z_OFFSET = 0

        sum_acc_x = 0
        sum_acc_y = 0
        sum_acc_z = 0
        sum_gyro_x = 0
        sum_gyro_y = 0
        sum_gyro_z = 0

        for i in range(120):
            acc_x, acc_y, acc_z = self.getACC()
            gyro_x, gyro_y, gyro_z = self.getGYRO()
            sum_acc_x += acc_x
            sum_acc_y += acc_y
            sum_acc_z += acc_z

            sum_gyro_x += gyro_x
            sum_gyro_y += gyro_y
            sum_gyro_z += gyro_z
            time.sleep(0.02)
        self.ACC_X_OFFSET = 0 - sum_acc_x/ 120
        self.ACC_Y_OFFSET = 0 - sum_acc_y / 120
        self.ACC_Z_OFFSET = 1 - sum_acc_z / 120
        self.GYRO_X_OFFSET = 0 - sum_gyro_x / 120
        self.GYRO_Y_OFFSET = 0 - sum_gyro_y / 120
        self.GYRO_Z_OFFSET = 0 - sum_gyro_z / 120

        _1553b['Calibrated'] = 0x7F  #已校准
        print("已校准，补偿值为",self.ACC_X_OFFSET,self.ACC_Y_OFFSET,self.ACC_Z_OFFSET,self.GYRO_X_OFFSET,self.GYRO_Y_OFFSET,self.GYRO_Z_OFFSET)
