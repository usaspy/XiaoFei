#!/usr/bin/python3
# coding=utf-8
import time
'''
从AK8963芯片获取地磁数据
注意：此程序要在MPU9255初始化完后执行
'''
class AK8963(object):
    I2C_SLV0_CTRL = 0x27
    I2C_SLV0_ADDR = 0x25
    I2C_SLV0_REG = 0x26
    USER_CTRL = 0x6a

    CNTL1 = 0x0A
    # 初始化AK8963芯片
    def __init__(self,bus,addr):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0x75, 1)
        if WHOAMI[0] == 0x73:
            # I2C Master方式读取地磁计
            bus.write_byte_data(self.addr,self.I2C_SLV0_CTRL,0x86)    #  0x80 | 8 启用第一个从机配置,读取6byte数据。10000110=接收6个字节的磁力计数据     https://www.cnblogs.com/leptonation/p/5225889.html
            bus.write_byte_data(self.addr,self.I2C_SLV0_REG,0x03)    #起始读取位置设置 0x00
            bus.write_byte_data(self.addr,self.I2C_SLV0_ADDR,0x8c)    #Slave 0 I2C Address    AK8963_I2C_ADDR | 0x80
            bus.write_byte_data(self.addr,self.USER_CTRL,0x20)    #I2C Master Mode Enable  启用
            # bus.write_byte_data(self.addr,self.USER_CTRL,0x16)    #连续测量模式 100Hz，16bit Output

            print("AK8963已设置为I2C Master模式")


    # 获取加速度A值 x,y,z
    def getMG(self):
        pass
