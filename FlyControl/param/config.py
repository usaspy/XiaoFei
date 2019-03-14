#!/usr/bin/python3
# coding=utf-8
'''
飞行控制器初始化参数设置
'''

#地面站IP
IPADDRESS_GS = "192.168.0.102"
#地面站控制链路端口(上行/TCP/长连接)
PORT_GS_CONTROL = 13130
#地面站数据链路端口(下行/UDP)
PORT_GS_DATA = 13133

#GY-99串口
SERIAL_PORT_GY99="/dev/ttyAMA0"

#GPS数据串口
SERIAL_PORT_GPS="/dev/ttyUSB2"

#GPRS拨号串口
SERIAL_PORT_GPRS="/dev/ttyUSB3"

#指南针补偿角度
COMPASS_COMPENSATE = -37.2

#动力系统  4轴初始油门 =0
MOTOR_01 = 0
MOTOR_02 = 0
MOTOR_03 = 0
MOTOR_04 = 0

#动力安全锁
MOTOR_LOCK = True





