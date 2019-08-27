#!/usr/bin/python3
# coding=utf-8
import time
'''
从AK8963芯片获取地磁数据
注意：此程序要在MPU9255初始化完后执行
'''
class AK8963x(object):
    AK8963_CNTL1 = 0x0A
    # 初始化AK8963芯片
    def __init__(self,bus,addr):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0x00, 1)
        if WHOAMI[0] == 0x48:
            #设置为连续测量模式 100Hz，16bit Output
            bus.write_byte_data(self.addr, self.AK8963_CNTL1, 0x16)  #https://wenku.baidu.com/view/7247cf7a5bcfa1c7aa00b52acfc789eb172d9e5e.html
            time.sleep(0.1)
            print("AK8963已开启——Pass Through Mode")

    # 获取地磁数据x,y,z
    def getMAG(self):
        mag = self.bus.read_i2c_block_data(self.addr, 0x03, 6)
        mag_x = ((mag[1] << 8) | mag[0])
        mag_y = ((mag[3] << 8) | mag[2])
        mag_z = ((mag[5] << 8) | mag[4])
        return mag_x,mag_y,mag_z
