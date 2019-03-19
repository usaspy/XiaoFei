#!/usr/bin/python3
# coding=utf-8
import serial
import time
import serial.tools.list_ports as ls_ports
import binascii

plist = ls_ports.comports()
print(type(plist))
if len(plist) > 0:
        print(list(plist[0]))

#打开串口
ser = serial.Serial(port="/dev/ttyAMA0",baudrate=115200,timeout=15,bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=1)
try:
    # 输出数据设置指令,0xFO=输出后四位参数
    cmd1=b'\xA5\x55\xF0\xEA'
    # 自动输出数据指令
    cmd2=b'\xA5\x56\x02\xFD'
    #波特率设置指=115200
    cmd3=b'\xA5\x58\x01\xFE'
    #设置刷新频率=10HZ
    cmd4=b'\xA5\x59\x01\xFF'
    #加速度陀螺仪校准指令
    cmd5=b'\xA5\x57\x01\xFD'
    #磁力计校准指令
    cmd6=b'\xA5\x57\x02\xFE'
    #保存设置
    cmd7=b'\xA5\x5A\x01\x00'
    #恢复出厂设置
    cmd8=b'\xA5\x5A\x02\x01'

    if ser.isOpen():
        print("-----------")
        ser.write(cmd1)
        time.sleep(0.5)

        ser.write(cmd2)
        time.sleep(0.5)

        ser.write(cmd3)
        time.sleep(0.5)

        ser.write(cmd4)
        time.sleep(0.5)


        ser.write(cmd5)
        time.sleep(0.5)
        ser.write(cmd6)
        time.sleep(0.5)

        ser.write(cmd7)
        time.sleep(0.5)

        while True:
            count = ser.inWaiting()
            #print(count)
            if count > 0 :
                rec = ser.read(count)
                print(binascii.b2a_hex(rec))
                #print(rec)

                ser.flushInput()
           # time.sleep(1)
except KeyboardInterrupt as e:
    print(e)
except Exception as ex:
    print(ex)
finally:
    ser.close()


