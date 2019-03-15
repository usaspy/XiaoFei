#!/usr/bin/python3
# coding=utf-8
'''
    四轴飞行器动力系统
    按顺时针方向排序
    01 03 一组
    02 04 一组
'''
import RPi.GPIO as GPIO
import time
from FlyControl.lib import libmotor
from FlyControl.param import config

#https://blog.csdn.net/qq_22169787/article/details/83379935
#开机后引擎状态初始化，然后设置安全锁
def motor_init(motors):
    GPIO.setmode(GPIO.BOARD)
    for motorId in motors:
        pin = config.MOTOR[motorId]['GPIO']
        GPIO.setup(pin, GPIO.OUT, initial=False)
        p = GPIO.PWM(pin, 50)
        p.start(libmotor.convert_power(0))
        config.MOTOR[motorId]['OBJ'] = p

#马达工作
def working():
    try:
        #马达初始化
        motor_init([1,2,3,4])

        while True:
            print("ready%s"% config.MOTOR)
            config.MOTOR[1]['OBJ'].ChangeDutyCycle(config.MOTOR[1]['CURR_POWER'])
            config.MOTOR[2]['OBJ'].ChangeDutyCycle(config.MOTOR[2]['CURR_POWER'])
            config.MOTOR[3]['OBJ'].ChangeDutyCycle(config.MOTOR[3]['CURR_POWER'])
            config.MOTOR[4]['OBJ'].ChangeDutyCycle(config.MOTOR[4]['CURR_POWER'])
            time.sleep(0.1)
    except Exception as e:
        print(e)
    finally:
        config.MOTOR[1]['OBJ'].stop()
        config.MOTOR[2]['OBJ'].stop()
        config.MOTOR[3]['OBJ'].stop()
        config.MOTOR[4]['OBJ'].stop()
        GPIO.cleanup(config.MOTOR[1]['GPIO'])
        GPIO.cleanup(config.MOTOR[2]['GPIO'])
        GPIO.cleanup(config.MOTOR[3]['GPIO'])
        GPIO.cleanup(config.MOTOR[4]['GPIO'])

#马达控制器工作
def controller(_1553b,_1553a):
    pass