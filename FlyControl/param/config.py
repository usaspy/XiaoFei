#!/usr/bin/python3
# coding=utf-8
'''
飞行控制器初始化参数设置
'''

#地面站IP
IPADDRESS_GS = "192.168.0.103"
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
#马达GPIO
#动力系统  4轴初始油门 =0 从1%~100%
#马达插脚
MOTOR1 = 29
MOTOR2 = 31
MOTOR3 = 33
MOTOR4 = 35

#马达实例
MOTOR1_OBJ = None
MOTOR2_OBJ = None
MOTOR3_OBJ = None
MOTOR4_OBJ = None

#当前油门 %百分比  0~100%
CURR_POWER = 0

#起飞油门 预计值
FLY_POWER=50

#引擎安全锁
FLY_LOCKED = True
#飞行状态
FLY_STATUS = 0   # 1: 'running' 0: 'stopped'

'''
用户操作变量 ,自稳时默认没有偏移量
前进时 设置俯仰角 = -30
后退时 设置俯仰角 = +30
左滑时 设置ROLL = -30
右滑时 设置ROLL = +30
转向时，设置YAW到指定得方位(需补偿COMPASS_OFFSET)
'''
ROLL_SET = 0
PITCH_SET = 0
YAW_SET = 0

#-------------------------------------------------高度指示器-----------------------------------------
Trig = 16
Echo = 18
