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

#开机后引擎状态初始化，然后设置安全锁
def motor_init(No):
    pin = libmotor.get_gpio(No)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT, initial=False)
    p = GPIO.PWM(pin, 50)
    p.start(libmotor.convert_power(0))

    return p

#马达工作
def working(No):
    try:
        #马达初始化
        p = libmotor.motor_init(No)

        while True:
            print("ready%s"% No)
            p.ChangeDutyCycle(libmotor.get_curr_power(No))
            time.sleep(0.1)
    except Exception as e:
        print(e)
    finally:
        p.stop()
        GPIO.cleanup(libmotor.get_gpio(No))

#马达控制器工作
def controller(_1553b,_1553a):
    pass