#电调 无刷电机测试

import RPi.GPIO as GPIO
import time

print("py:%s"%GPIO.VERSION)

GPIO.setmode(GPIO.BOARD)
ctl_1 = 29
ctl_2 = 31
ctl_3 = 33
ctl_4 = 35

GPIO.setup(ctl_1,GPIO.OUT,initial=False)
GPIO.setup(ctl_2,GPIO.OUT,initial=False)
GPIO.setup(ctl_3,GPIO.OUT,initial=False)
GPIO.setup(ctl_4,GPIO.OUT,initial=False)
p1 = GPIO.PWM(ctl_1,50)
p2 = GPIO.PWM(ctl_2,50)
p3 = GPIO.PWM(ctl_3,50)
p4 = GPIO.PWM(ctl_4,50)

p1.start(10)
p2.start(10)
p3.start(10)
p4.start(10)
time.sleep(10)
p1.ChangeDutyCycle(5)
p2.ChangeDutyCycle(5)
p3.ChangeDutyCycle(5)
p4.ChangeDutyCycle(5)
time.sleep(2)
p1.ChangeDutyCycle(5)
p2.ChangeDutyCycle(5)
p3.ChangeDutyCycle(5)
p4.ChangeDutyCycle(5)
time.sleep(3)
p1.ChangeDutyCycle(7)
p2.ChangeDutyCycle(7)
p3.ChangeDutyCycle(7)
p4.ChangeDutyCycle(7)

while True:
   p1.ChangeDutyCycle(6)
   p2.ChangeDutyCycle(6)
   p3.ChangeDutyCycle(6)
   p4.ChangeDutyCycle(6)
   print("------")
   time.sleep(1)

p.stop()
GPIO.cleanup()

