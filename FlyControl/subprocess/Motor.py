#!/usr/bin/python3
# coding=utf-8
'''
    四轴飞行器动力系统
    按顺时针方向排序
    1 3 一组
    2 4 一组
'''
import RPi.GPIO as GPIO
import time
from FlyControl.lib import libmotor
from FlyControl.lib import PIDv2
from FlyControl.param import config as cfg
from FlyControl.lib.PID import PID

#https://blog.csdn.net/qq_22169787/article/details/83379935
#开机后引擎状态初始化，然后设置安全锁
def __motor_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(cfg.MOTOR1, GPIO.OUT, initial=False)
    GPIO.setup(cfg.MOTOR2, GPIO.OUT, initial=False)
    GPIO.setup(cfg.MOTOR3, GPIO.OUT, initial=False)
    GPIO.setup(cfg.MOTOR4, GPIO.OUT, initial=False)

    p1 = GPIO.PWM(cfg.MOTOR1, 50)
    p2 = GPIO.PWM(cfg.MOTOR2, 50)
    p3 = GPIO.PWM(cfg.MOTOR3, 50)
    p4 = GPIO.PWM(cfg.MOTOR4, 50)

    p1.start(libmotor.real_pwm(0))
    p2.start(libmotor.real_pwm(0))
    p3.start(libmotor.real_pwm(0))
    p4.start(libmotor.real_pwm(0))
    time.sleep(2)

    cfg.MOTOR1_OBJ = p1
    cfg.MOTOR2_OBJ = p2
    cfg.MOTOR3_OBJ = p3
    cfg.MOTOR4_OBJ = p4

'''
飞行控制器主线程 
大循环

1）系统开机后首先初始化所有马达，马达油门归零
2）if FLY_LOCKED = False and FLY_STATUS = 1 计算自平衡时的PID值，然后马达执行步长=1
3）if FLY_LOCKED = True  只输出PID值，马达不执行
4）if FLY_LOCKED = False and 
'''
def controller(_1553b,_1553a):
    try:
        #马达初始化
        __motor_init()
        #初始化PID引擎
        pid = PID()
        while True:
            pid.calculate(_1553b,_1553a)
            cfg.MOTOR1_OBJ.ChangeDutyCycle(libmotor.real_pwm(cfg.MOTOR1_POWER))
            cfg.MOTOR2_OBJ.ChangeDutyCycle(libmotor.real_pwm(cfg.MOTOR2_POWER))
            cfg.MOTOR3_OBJ.ChangeDutyCycle(libmotor.real_pwm(cfg.MOTOR3_POWER))
            cfg.MOTOR4_OBJ.ChangeDutyCycle(libmotor.real_pwm(cfg.MOTOR4_POWER))
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        cfg.MOTOR1_OBJ.stop()
        cfg.MOTOR2_OBJ.stop()
        cfg.MOTOR3_OBJ.stop()
        cfg.MOTOR4_OBJ.stop()
        GPIO.cleanup(cfg.MOTOR1)
        GPIO.cleanup(cfg.MOTOR2)
        GPIO.cleanup(cfg.MOTOR3)
        GPIO.cleanup(cfg.MOTOR4)