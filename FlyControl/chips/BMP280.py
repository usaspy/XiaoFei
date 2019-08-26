#!/usr/bin/python3
# coding=utf-8
'''
从BMP280传感器获取温度、气压值
'''
import time

class BMP280x(object):
    CTRL_MEAS = 0xF4    #测量控制寄存器  https://blog.csdn.net/sunshinebooming/article/details/79637822
    RESET = 0xE0  #复位寄存器
    BMP280_TEMP_ADDR = 0xfa
    BMP280_PRESS_ADDR = 0xf7

    # 初始化BMP280芯片
    def __init__(self,bus,addr):
        self.bus = bus
        self.addr = addr
        WHOAMI = bus.read_i2c_block_data(addr, 0xd0, 1)
        if WHOAMI[0] == 0x58:
            bus.write_byte_data(self.addr, self.RESET, 0xB6)  # 电源管理,复位BMP280
            time.sleep(0.2)
            bus.write_byte_data(self.addr, self.CTRL_MEAS, 0xFF)  # 设置采集温度、气压的精度

            self.dig_T1 = self.__bmp280_MultipleReadTwo(0x88)
            self.dig_T2 = self.__bmp280_MultipleReadTwo(0x8A)
            self.dig_T3 = self.__bmp280_MultipleReadTwo(0x8C)
            self.dig_P1 = self.__bmp280_MultipleReadTwo(0x8E)
            self.dig_P2 = self.__bmp280_MultipleReadTwo(0x90)
            self.dig_P3 = self.__bmp280_MultipleReadTwo(0x92)
            self.dig_P4 = self.__bmp280_MultipleReadTwo(0x94)
            self.dig_P5 = self.__bmp280_MultipleReadTwo(0x96)
            self.dig_P6 = self.__bmp280_MultipleReadTwo(0x98)
            self.dig_P7 = self.__bmp280_MultipleReadTwo(0x9A)
            self.dig_P8 = self.__bmp280_MultipleReadTwo(0x9C)
            self.dig_P9 = self.__bmp280_MultipleReadTwo(0x9E)
            time.sleep(0.2)

            print("BMP280初始化完成")

    def __bmp280_MultipleReadTwo(self,loc):
        data = self.bus.read_i2c_block_data(self.addr,loc,2);
        return (data[1] << 8) | data[0]

    def __bmp280_MultipleReadThree(self,loc):
        data = self.bus.read_i2c_block_data(self.addr,loc,3);
        return (data[0] << 12) | (data[1] << 4 )| (data[2] >> 4)

    # 获取温度和气压数据
    def getTEMP_PRESS(self):
        adc_T = self.__bmp280_MultipleReadThree(self.BMP280_TEMP_ADDR)
        adc_P = self.__bmp280_MultipleReadThree(self.BMP280_PRESS_ADDR)
        #温度
        var1 = (adc_T/ 16384.0 - self.dig_T1 / 1024.0) * self.dig_T2
        var2 = ((adc_T / 131072.0 - self.dig_T1 / 8192.0) * (adc_T / 131072.0 - self.dig_T1 / 8192.0) ) * self.dig_T3

        t_fine = var1 + var2

        T = var1+var2/5120.0

        #气压
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = (var2 / 4.0) + (self.dig_P4 * 65536.0)
        var1 = ((self.dig_P3) * var1 * var1 / 524288.0 + (self.dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (self.dig_P1)
        p = 1048576.0 - adc_P
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (self.dig_P9) * p * p / 2147483648.0
        var2 = p * (self.dig_P8) / 32768.0
        p = p + (var1 + var2 + (self.dig_P7)) / 16.0

        return T,p
