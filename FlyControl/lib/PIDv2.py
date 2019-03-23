"""
双环串级PID反馈控制：
                外环输入：欧拉角（X，Y，Z）
                外环输出：期望角速度
                内环输入：期望角速度-当前陀螺仪测量的角速度（X，Y，Z）
                内环输出：PWM信号补偿控制电机
"""
import time
from FlyControl.param import config as cfg

def engine_fly(_1553b,_1553a):
    #外环输入：欧拉角的上一次误差
    x_last = 0.0
    y_last = 0.0
    z_last = 0.0
    #外环输入：欧拉角的积分参数
    x_sum = 0.0
    y_sum = 0.0
    z_sum = 0.0
    #外环输出：角速度期望值
    xv_et = 0.0
    yv_et = 0.0
    zv_et = 0.0
    #内环输入：角速度的上一次误差
    xv_last = 0.0
    yv_last = 0.0
    zv_last = 0.0
    #内环输入：角速度的积分参数
    xv_sum = 0.0
    yv_sum = 0.0
    zv_sum = 0.0

    while True:
        # 传感器测量的当前角度
        x_curr =  _1553b['ROLL']
        y_curr =  _1553b['PITCH']
        z_curr =  _1553b['YAW']
        # 传感器测量的当前角速度
        xv_curr = _1553b['GYRO_X']
        yv_curr = _1553b['GYRO_Y']
        zv_curr = _1553b['GYRO_Z']

        #外环PID根据欧拉角计算出期望角速度
        #这里应该是期望角度 - 当前实际角度，所以这里为 0 - x_et
        xv_et = engine_outside_pid(-x_curr, -x_last, x_sum)
        yv_et = engine_outside_pid(-y_curr, -y_last, y_sum)
        zv_et = engine_outside_pid(-z_curr, -z_last, None)

        #内环输入调整：实际期望角速度 = 期望角速度 - 当前角速度 （补偿当前角速度）
        xv_et -= xv_curr
        yv_et -= yv_curr
        zv_et -= zv_curr

        #内环PID根据角速度误差计算出PWM调整量
        x_pwm = engine_inside_pid(xv_et, xv_last, xv_sum)
        y_pwm = engine_inside_pid(yv_et, yv_last, yv_sum)
        z_pwm = engine_inside_pid(zv_et, zv_last, None)

        #记录欧拉角的上一次读数
        x_last = x_curr
        y_last = y_curr
        z_last = z_curr

        #记录角速度的上一次读数
        xv_last = xv_et
        yv_last = yv_et
        zv_last = zv_et

        motor_process(_1553b,x_pwm,y_pwm,z_pwm)

        #电机每0.1秒调整一次
        time.sleep(0.1)
'''
外环PID输入角度输出角速度
et:当前角度误差
et2:上一次角度误差
输出：期望角速度
'''
def engine_outside_pid(et,et2,sum):
    #输出期望角速度
    palstance = 0.0
    if sum == None:
        #Z轴PID中只做P和D
        palstance = cfg.kp * et + cfg.kd * (et - et2)
        palstance = engine_limit_palstance(palstance)
        return palstance
    sum += cfg.ki * et * 0.01
    #积分限幅
    sum = engine_limit_palstance(sum)
    #XY轴PID反馈控制
    palstance = cfg.kp * et + sum + cfg.kd * (et - et2)
    #输出限幅
    palstance = engine_limit_palstance(palstance)
    return palstance

'''
内环PID输入角速度输出PWM
et:当前角速度误差
et2:上一次角速度误差
输出：PWM调整值
'''
def engine_inside_pid(et,et2,sum):
    #输出期望PWM值
    pwm = 0.0
    if sum == None:
        pwm = cfg.v_kp * et + cfg.v_kd * (et -et2)
        engine_limit_pwm(pwm)
        return pwm
    sum += cfg.v_ki * et * 0.01
    engine_limit_pwm(sum)
    pwm = cfg.v_kp * et + sum + cfg.v_kd * (et - et2)
    engine_limit_pwm(pwm)
    return pwm

#外环角速度限幅
def engine_limit_palstance(palstance):
    MAX_PALSTANCE = 40  #允许的最大角速度（度/秒）
    if palstance > MAX_PALSTANCE:
        return MAX_PALSTANCE
    elif 0 <= palstance <= MAX_PALSTANCE:
        return palstance
    elif -MAX_PALSTANCE < palstance < 0:
        return palstance
    elif palstance < -MAX_PALSTANCE:
        return -MAX_PALSTANCE


#内环PWM限幅
#实际限制的是油门0~100%,最
def engine_limit_pwm(pwm):
    MAX_PWM = 100  # 油门大小：0~100%
    if pwm > MAX_PWM:
        return MAX_PWM
    elif 0 <= pwm <= MAX_PWM:
        return pwm
    elif -MAX_PWM < pwm < 0:
        return pwm
    elif pwm < -MAX_PWM:
        return -MAX_PWM

'''
PWM发送到1553b总线，交给电机执行
'''
def motor_process(_1553b,x_pwm,y_pwm,z_pwm):
    pass