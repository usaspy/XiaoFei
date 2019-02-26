#电调 无刷电机测试

import RPi.GPIO as GPIO
import time

print("py:%s"%GPIO.VERSION)

GPIO.setmode(GPIO.BOARD)
ctl_1 = 11

GPIO.setup(ctl_1,GPIO.OUT,initial=False)
p = GPIO.PWM(ctl_1,50)
p.start(10)
time.sleep(20)
p.ChangeDutyCycle(5)
time.sleep(2)
p.ChangeDutyCycle(5)
time.sleep(3)
p.ChangeDutyCycle(7)

while True:
   p.ChangeDutyCycle(6)
   print("------")
   time.sleep(1)

p.stop()
GPIO.cleanup()

