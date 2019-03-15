from FlyControl.param import config
import RPi.GPIO as GPIO
import time

#得到指定马达的当前油门值
def get_curr_power(No):
    if No == 1:
        return config.CURR_POWER_01
    if No == 2:
        return config.CURR_POWER_02
    if No == 3:
        return config.CURR_POWER_03
    if No == 4:
        return config.CURR_POWER_04
    return None

#设置指定马达的当前油门值
def set_curr_power(No,new_value):
    if No == 1:
        config.CURR_POWER_01 = new_value
    if No == 2:
        config.CURR_POWER_02 = new_value
    if No == 3:
        config.CURR_POWER_03 = new_value
    if No == 4:
        config.CURR_POWER_04 = new_value

#获取指定马达的GPIO号
def get_gpio(No):
    if No == 1:
        return config.MOTOR_01_GPIO
    if No == 2:
        return config.MOTOR_02_GPIO
    if No == 3:
        return config.MOTOR_03_GPIO
    if No == 4:
        return config.MOTOR_04_GPIO
    return None

#换算成马达的PWM值 传入电调 油门范围在0%~100%之间
def convert_power(curr_power):
    #输入电调的PWM值
    v = (100 + curr_power)/20
    #由于接了光耦模块，故取反 用100-v
    return 100 - v

#开机后引擎状态初始化，然后设置安全锁
def motor_init(No):
    pin = get_gpio(No)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT, initial=False)
    p = GPIO.PWM(pin, 50)
    p.start(convert_power(0))

    return p



