'''
地高传感器
测量无人机悬停时得离地高度
量程：2CM——450CM

'''

import RPi.GPIO as GPIO
from FlyControl.param import config as cfg

import time
GPIO.setmode(GPIO.BOARD)
#超声波初始化
GPIO.setup(cfg.Trig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(cfg.Echo, GPIO.IN)

# 开始测距
GPIO.output(cfg.Trig, GPIO.HIGH)
time.sleep(0.01)
GPIO.output(cfg.Trig, GPIO.LOW)

#改成事件监听更省资源
while GPIO.input(cfg.Echo) == GPIO.LOW:
    pass

starttime = time.time()

while GPIO.input(cfg.Echo) == GPIO.HIGH:
    pass

endtime = time.time()

distance = 340 * (endtime - starttime) / 2

print(distance)