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
from FlyControl.lib import libmotor as lm
from FlyControl.param import config as cfg
from FlyControl.lib.PID import PID

'''
timeit测试性能
https://blog.csdn.net/qq_22169787/article/details/83379935
'''

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
    time.sleep(1)

    p1.start(lm.real_pwm(0))
    p2.start(lm.real_pwm(0))
    p3.start(lm.real_pwm(0))
    p4.start(lm.real_pwm(0))
    time.sleep(5) #等待5秒，确保电调初始化完成

    cfg.MOTOR1_OBJ = p1
    cfg.MOTOR2_OBJ = p2
    cfg.MOTOR3_OBJ = p3
    cfg.MOTOR4_OBJ = p4

'''
飞行控制器主线程 
大循环
'''
def controller(_1553b,_1553a):
    try:
        #初始化四轴马达
        __motor_init()
        #初始化PID引擎
        pid = PID()
        #大循环
        while True:
            if cfg.FLY_LOCKED is False:  #如果安全锁打开，则允许飞行
                cmd = _1553a.pop(0) if _1553a else None
                if cmd == b'\x20\x19\x04\xFE':  # 上锁
                    cfg.FLY_LOCKED = True
                    continue
                elif cmd == b'\x20\x19\x09\xA7':  # 紧急降落
                    #执行紧急降落程序
                    #阻塞
                    lm.exec_plan_b(cfg)
                    break
                elif cmd == b'O': #加油门 每一个O 油门+1
                    cfg.CURR_POWER = lm.limit_power_range(cfg.CURR_POWER + 1)
                elif cmd == b'P': #减油门
                    cfg.CURR_POWER = lm.limit_power_range(cfg.CURR_POWER - 1)
                elif cmd == b'K': #持续左转
                    # 修改期望角度
                    cfg.ROLL_SET = 0
                    cfg.PITCH_SET = 0
                    cfg.YAW_SET = -45 #################################
                elif cmd == b'L': #持续右转
                    # 修改期望角度
                    cfg.ROLL_SET = 0
                    cfg.PITCH_SET = 0
                    cfg.YAW_SET = +45 #################################
                elif cmd == b'W': #设置前倾30°，前进
                    #修改期望角度
                    cfg.ROLL_SET = 0
                    cfg.PITCH_SET = -25
                    cfg.YAW_SET = 0
                elif cmd == b'S': #设置后倾30°，后退
                    # 修改期望角度
                    cfg.ROLL_SET = 0
                    cfg.PITCH_SET = +25
                    cfg.YAW_SET = 0
                elif cmd != None and cmd[0:4] == b'\x20\x19\x10\x0e':  # 调试模式：设置PID参数
                    pids = eval(cmd[4:].decode("utf-8"))
                    pid.kp = float(pids[0])
                    pid.ki = float(pids[1])
                    pid.kd = float(pids[2])
                    pid.v_kp = float(pids[3])
                    pid.v_ki = float(pids[4])
                    pid.v_kd = float(pids[5])
                else: #当前没有新指令,或输入了无效指令时，维持自稳状态
                    cfg.ROLL_SET = 0
                    cfg.PITCH_SET = 0
                    cfg.YAW_SET = 0
                x_pwm,y_pwm,z_pwm = pid.calculate(_1553b) #双环PID计算电机调整量
                set_power(x_pwm,y_pwm,z_pwm) #发送PWM调整量给电调执行
                _1553b['CURR_POWER'] = cfg.CURR_POWER #更新1553B数据总线中得当前油门值
                time.sleep(0.01)  #经过计算以上程序0.005秒内执行完，延迟0.01秒 ，频率= 0.015秒， GY99 频率为50HZ 0.02秒，基本合适
            else: #如果安全锁关闭，则不能执行任何飞行指令
                cmd = _1553a.pop(0) if _1553a else None
                if cmd == b'\x20\x19\x04\xFD': #开锁
                    cfg.FLY_LOCKED = False
                    #指南针补偿角
                    cfg.COMPASS_OFFSET = int(_1553b.get('YAW', 0))
                if cmd == b'\x20\x19\x07\xFF': #电机测试
                    lm.test_motor(cfg)
                time.sleep(2)
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


'''
    根据x、y、z方向上的补偿值计算每个电机实际调整幅度
'''
def set_power(x_pwm, y_pwm, z_pwm):
    #当前油门低于起飞油门 （<50%）就不进行PID油门调整
    #并且在起飞之前不做积分，避免还没起飞就累积了较大误差
    if cfg.CURR_POWER  < cfg.FLY_POWER:
        x_pwm = 0
        y_pwm = 0
        z_pwm = 0
    # X型 计算四个电机的PWM值
    MOTOR1_POWER = lm.limit_power_range(cfg.CURR_POWER + x_pwm/2 + y_pwm/2 - z_pwm)
    MOTOR2_POWER = lm.limit_power_range(cfg.CURR_POWER + x_pwm/2 - y_pwm/2 + z_pwm)
    MOTOR3_POWER = lm.limit_power_range(cfg.CURR_POWER - x_pwm/2 - y_pwm/2 - z_pwm)
    MOTOR4_POWER = lm.limit_power_range(cfg.CURR_POWER - x_pwm/2 + y_pwm/2 + z_pwm)
    #设置四个电机的PWM
    cfg.MOTOR1_OBJ.ChangeDutyCycle(lm.real_pwm(MOTOR1_POWER))
    cfg.MOTOR2_OBJ.ChangeDutyCycle(lm.real_pwm(MOTOR2_POWER))
    cfg.MOTOR3_OBJ.ChangeDutyCycle(lm.real_pwm(MOTOR3_POWER))
    cfg.MOTOR4_OBJ.ChangeDutyCycle(lm.real_pwm(MOTOR4_POWER))

    #print("%f,%f,%f,%f" % (MOTOR1_POWER, MOTOR2_POWER, MOTOR3_POWER, MOTOR4_POWER))