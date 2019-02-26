#电调 无刷电机测试

import RPi.GPIO as GPIO
import time

print("py:%s"%GPIO.VERSION)

GPIO.setmode(GPIO.BOARD)
ctl_1 = 11

GPIO.setup(ctl_1,GPIO.OUT,initial=False)
p = GPIO.PWM(ctl_1,50)
p.start(5)
time.sleep(5)

print("--60%--10sec--")
p.ChangeDutyCycle(6)
time.sleep(10)
print("--90%--5sec--")
p.ChangeDutyCycle(9)
time.sleep(5)
print("--stop--2sec--")
p.ChangeDutyCycle(5)
time.sleep(2)
print("---100%--5sec-")
p.ChangeDutyCycle(10)
time.sleep(5)
print("---STOP---")

p.ChangeDutyCycle(5)
p.stop()
GPIO.cleanup()

