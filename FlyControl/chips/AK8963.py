#!/usr/bin/python3
# coding=utf-8
import time
'''
从AK8963芯片获取地磁数据
注意：此程序要在MPU9255初始化完后执行
https://wenku.baidu.com/view/7247cf7a5bcfa1c7aa00b52acfc789eb172d9e5e.html
https://blog.csdn.net/u013256018/article/details/52795043
'''
class AK8963x(object):
    AK8963_CNTL1 = 0x0A
    AK8963_REST = 0x0B

    ASAX = 0
    ASAY = 0
    ASAZ = 0
    # 初始化AK8963芯片
    def __init__(self,bus,addr):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0x00, 1)
        if WHOAMI[0] == 0x48:
            time.sleep(0.5)
            #重启REST
            bus.write_byte_data(self.addr, self.AK8963_REST, 0x01)
            time.sleep(0.2)
            # 进入Fuse ROM access mode，读取校准值
            self.__read_ASA_Value()
            #设置为连续测量模式 100Hz，16bit Output
            bus.write_byte_data(self.addr, self.AK8963_CNTL1, 0x16)
            time.sleep(0.1)
            print("AK8963已开启——Pass Through Mode")

    # 获取地磁数据x,y,z
    def getMAG(self):
        mag = self.bus.read_i2c_block_data(self.addr, 0x03, 6)
        #在连续模式下，每次读完数据必须读一下st2寄存器地址，这样9250才会刷新新的数据。不然他会认为你没有读完，就会处于锁定状态。
        self.bus.read_i2c_block_data(self.addr, 0x09, 6)
        mag_x = ((mag[1] << 8) | mag[0])
        mag_y = ((mag[3] << 8) | mag[2])
        mag_z = ((mag[5] << 8) | mag[4])

        #校准后输出    Hadj = H * (((ASA - 128) * 0.5 / 128) + 1)
        mag_x = self.__hex2dec(mag_x) * (((self.ASAX - 128) * 0.5 / 128) + 1)
        mag_y = self.__hex2dec(mag_y) * (((self.ASAY - 128) * 0.5 / 128) + 1)
        mag_z = self.__hex2dec(mag_z) * (((self.ASAZ - 128) * 0.5 / 128) + 1)
        return mag_x,mag_y,mag_z

    # 进入Fuse ROM access mode，读取校准值
    def __read_ASA_Value(self):
        self.bus.write_byte_data(self.addr, self.AK8963_CNTL1, 0x1F)
        time.sleep(0.5)
        ASA = self.bus.read_i2c_block_data(self.addr, 0x10, 3)
        self.ASAX = ASA[0]
        self.ASAY = ASA[1]
        self.ASAZ = ASA[2]

    # 根据十六进制数转化为带符号的十进制数
    # 最高位是符号位，最高为位1是负数， 为0是正数
    def __hex2dec(self,d):
        if d & 0x8000 == 0x8000:
            d = d ^ 0xFFFF  # 异或，相同为0，不同为1
            d = ~d  # ~符号表示运算：~d = -(d+1)
        return d
