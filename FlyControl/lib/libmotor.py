from FlyControl.param import config
import time

#设置指定马达的当前油门值
def set_curr_power(No,new_value):
    config.MOTOR[No]['CURR_POWER'] = new_value

'''
油门限制，在5%~95%之间
'''
def limit_power_range(power):
    MIN_POWER=5
    MAX_POWER=95
    if power > MAX_POWER:
        return MAX_POWER
    if power < MIN_POWER:
        return MIN_POWER
    return power



#换算成马达的PWM值 传入电调 油门范围在0%~100%之间
def real_pwm(curr_power):
    #输入电调的PWM值
    v = (100 + curr_power)/20
    #由于接了光耦模块，故取反 用100-v
    return 100 - v


def exec_plan_b(cfg):
    cfg.CURR_POWER = 0
    pass


def output_to_datalog(data):
    with open('/data.log', 'a') as f:
        f.write(data + '\n')

#电机测试
def test_motor(cfg):
    cfg.MOTOR1_OBJ.ChangeDutyCycle(real_pwm(10))
    time.sleep(3)
    cfg.MOTOR1_OBJ.ChangeDutyCycle(real_pwm(0))

    cfg.MOTOR2_OBJ.ChangeDutyCycle(real_pwm(10))
    time.sleep(3)
    cfg.MOTOR2_OBJ.ChangeDutyCycle(real_pwm(0))

    cfg.MOTOR3_OBJ.ChangeDutyCycle(real_pwm(10))
    time.sleep(3)
    cfg.MOTOR3_OBJ.ChangeDutyCycle(real_pwm(0))

    cfg.MOTOR4_OBJ.ChangeDutyCycle(real_pwm(10))
    time.sleep(3)
    cfg.MOTOR4_OBJ.ChangeDutyCycle(real_pwm(0))

