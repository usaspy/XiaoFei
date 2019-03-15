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

#指南针偏移量
COMPASS_OFFSET = -37.2


#-------------------------------------------------飞控变量-----------------------------------------
MOTOR = {}
#马达GPIO
MOTOR[1]['GPIO'] = 29
MOTOR[2]['GPIO'] = 31
MOTOR[3]['GPIO'] = 33
MOTOR[4]['GPIO'] = 35

#动力系统  4轴初始油门 =0 从1%~100%
MOTOR[1]['CURR_POWER'] = 0
MOTOR[2]['CURR_POWER'] = 0
MOTOR[3]['CURR_POWER'] = 0
MOTOR[4]['CURR_POWER'] = 0


#动力安全锁
MOTOR_LOCK = True

FLY_MODE='test'   #'work' or 'test'





