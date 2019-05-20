#电调 无刷电机测试程序
#这是接了光耦隔离后的
import RPi.GPIO as GPIO
import time

print("py:%s"%GPIO.VERSION)

GPIO.setmode(GPIO.BOARD)
ctl_1 = 29  #树莓派上29针脚
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

p1.start(95)
p2.start(95)
p3.start(95)
p4.start(95)

print("95")
p1.ChangeDutyCycle(95)
p1.ChangeDutyCycle(95)
p1.ChangeDutyCycle(95)
p1.ChangeDutyCycle(95)
time.sleep(2)

print("---20%--5sec-")
p1.ChangeDutyCycle(94)
p2.ChangeDutyCycle(94)
p3.ChangeDutyCycle(94)
p4.ChangeDutyCycle(94)
time.sleep(5)


p1.stop()
p2.stop()
p3.stop()
p4.stop()
GPIO.cleanup()

