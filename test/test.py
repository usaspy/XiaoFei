#电调 无刷电机测试
#这是接了光耦隔离后的
import RPi.GPIO as GPIO
import time

print("py:%s"%GPIO.VERSION)

GPIO.setmode(GPIO.BOARD)
ctl_1 = 11

GPIO.setup(ctl_1,GPIO.OUT,initial=False)
p = GPIO.PWM(ctl_1,50)
print("99")
p.start(99)
time.sleep(5)

print("100")
p.ChangeDutyCycle(100)
time.sleep(3)

print("96")
p.ChangeDutyCycle(96)
time.sleep(2)

print("95")
p.ChangeDutyCycle(95)
time.sleep(2)

print("---20%--5sec-")
p.s(94)
time.sleep(5)
print("40%")
p.ChangeDutyCycle(93)
time.sleep(3)
print("60%")
p.ChangeDutyCycle(92)
time.sleep(2)
print("80%")
p.ChangeDutyCycle(91)
time.sleep(3)
print("---100%----5sec-")
p.ChangeDutyCycle(90)
time.sleep(5)
print("---STOP---")

p.ChangeDutyCycle(5)
p.stop()
GPIO.cleanup()

