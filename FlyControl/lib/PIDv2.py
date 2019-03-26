"""
双环串级PID反馈控制：
                外环输入：欧拉角（X，Y，Z）
                外环输出：期望角速度
                内环输入：期望角速度-当前陀螺仪测量的角速度（X，Y，Z）
                内环输出：PWM信号补偿控制电机
"""
import time
from FlyControl.param import config as cfg

def calculate(_1553b,_1553a):
    #外环输入：欧拉角的上一次误差
    x_last = 0.0
    y_last = 0.0
    z_last = 0.0
    #外环输入：欧拉角的积分参数
    x_sum = [0.0]
    y_sum = [0.0]
    z_sum = [0.0]
    #外环输出：角速度期望值
    xv_et = 0.0
    yv_et = 0.0
    zv_et = 0.0
    #内环输入：角速度的上一次误差
    xv_last = 0.0
    yv_last = 0.0
    zv_last = 0.0
    #内环输入：角速度的积分参数
    xv_sum = [0.0]
    yv_sum = [0.0]
    zv_sum = [0.0]

    while True:
        # 传感器测量的当前角度
        x_curr =  _1553b.get('ROLL',0)
        y_curr =  _1553b.get('PITCH',0)
        z_curr =  _1553b.get('YAW',0)
        # 传感器测量的当前角速度
        xv_curr = _1553b.get('GYRO_X',0)
        yv_curr = _1553b.get('GYRO_Y',0)
        zv_curr = _1553b.get('GYRO_Z',0)

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

        set_power(x_pwm,y_pwm,z_pwm)

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
        palstance = [cfg.kp * et + cfg.kd * (et - et2)]
        engine_limit_palstance(palstance)
        return palstance[0]
    sum[0] += cfg.ki * et * 0.01
    #积分限幅
    engine_limit_palstance(sum)
    #XY轴PID反馈控制
    palstance = [cfg.kp * et + sum[0] + cfg.kd * (et - et2)]
    #输出限幅
    engine_limit_palstance(palstance)
    return palstance[0]

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
        pwm = [cfg.v_kp * et + cfg.v_kd * (et -et2)]
        engine_limit_pwm(pwm)
        return pwm[0]
    sum[0] += cfg.v_ki * et * 0.01
    engine_limit_pwm(sum)
    pwm = [cfg.v_kp * et + sum[0] + cfg.v_kd * (et - et2)]
    engine_limit_pwm(pwm)
    return pwm[0]

#外环角速度限幅
def engine_limit_palstance(val):
    MAX_PALSTANCE = 40  #允许的最大角速度（度/秒）
    if val[0] > MAX_PALSTANCE:
        val[0] = MAX_PALSTANCE
    elif val[0] < -MAX_PALSTANCE:
        val[0] = -MAX_PALSTANCE


#内环PWM限幅
#实际限制的是油门的15%,
def engine_limit_pwm(pwm):
    MAX_PWM = 15  # 对油门的调整幅度不能超过15%
    if pwm[0] > MAX_PWM:
        pwm[0] = MAX_PWM
    elif pwm[0] < -MAX_PWM:
        pwm[0] = -MAX_PWM

'''
根据x、y、z方向上的补偿值计算每个电机实际调整幅度
'''
def set_power(x_pwm,y_pwm,z_pwm):
    cfg.MOTOR1_POWER = cfg.MOTOR1_POWER + x_pwm - z_pwm
    cfg.MOTOR2_POWER = cfg.MOTOR2_POWER + y_pwm + z_pwm
    cfg.MOTOR3_POWER = cfg.MOTOR3_POWER - x_pwm - z_pwm
    cfg.MOTOR4_POWER = cfg.MOTOR4_POWER - y_pwm + z_pwm

    print("MOTOR1=%d,MOTOR2=%d,MOTOR3=%d,MOTOR4=%d"%(cfg.MOTOR1_POWER,cfg.MOTOR2_POWER,cfg.MOTOR3_POWER,cfg.MOTOR4_POWER))