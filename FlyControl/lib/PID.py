"""
双环串级PID反馈控制：
                外环输入：欧拉角（X，Y，Z）
                外环输出：期望角速度
                内环输入：期望角速度-当前陀螺仪测量的角速度（X，Y，Z）
                内环输出：PWM信号补偿控制电机
"""
import time
from FlyControl.param import config as cfg
from FlyControl.lib import libmotor as lm

class PID(object):
    # 外环输入：欧拉角的上一次误差
    x_last = 0.0
    y_last = 0.0
    z_last = 0.0
    # 外环输入：欧拉角的积分变量  累计误差
    x_sum = [0.0]
    y_sum = [0.0]
    z_sum = [0.0]
    # 外环输出：角速度期望值
    xv_et = 0.0
    yv_et = 0.0
    zv_et = 0.0
    # 内环输入：角速度的上一次误差
    xv_last = 0.0
    yv_last = 0.0
    zv_last = 0.0
    # 内环输入：角速度的积分变量  累计误差
    xv_sum = [0.0]
    yv_sum = [0.0]
    zv_sum = [0.0]
    def __init__(self):
        # 外环pid参数
        self.kp = 0.6
        self.ki = 0.1
        self.kd = 0.4
        # 内环pid参数
        self.v_kp = 0.3
        self.v_ki = 0.005
        self.v_kd = 0.5

    # 外环角速度限幅
    def engine_limit_palstance(self,val):
        MAX_PALSTANCE = 60  # 允许的最大角速度（度/秒）
        if val > MAX_PALSTANCE:
            return MAX_PALSTANCE
        elif val < -MAX_PALSTANCE:
            return -MAX_PALSTANCE
        return val

    # 内环PWM限幅
    # 油门调整限幅不超过20%
    def engine_limit_pwm(self,pwm):
        MAX_PWM = 20  # 对油门的调整幅度不能超过20%
        if pwm > MAX_PWM:
            return MAX_PWM
        elif pwm < -MAX_PWM:
            return -MAX_PWM
        return pwm
    '''
    根据x、y、z方向上的补偿值计算每个电机实际调整幅度
    '''
    def set_power(self,x_pwm, y_pwm, z_pwm):
        cfg.MOTOR1_POWER = lm.limit_power_range(cfg.MOTOR1_POWER + x_pwm - z_pwm)
        cfg.MOTOR2_POWER = lm.limit_power_range(cfg.MOTOR2_POWER + y_pwm + z_pwm)
        cfg.MOTOR3_POWER = lm.limit_power_range(cfg.MOTOR3_POWER - x_pwm - z_pwm)
        cfg.MOTOR4_POWER = lm.limit_power_range(cfg.MOTOR4_POWER - y_pwm + z_pwm)

        #print("油门调整幅度：X_PWM=%d,Y_PWM=%d,Z_PWM=%d" % (x_pwm,y_pwm,z_pwm))
        #print("调整后的油门：MOTOR1=%d,MOTOR2=%d,MOTOR3=%d,MOTOR4=%d" % (cfg.MOTOR1_POWER, cfg.MOTOR2_POWER, cfg.MOTOR3_POWER, cfg.MOTOR4_POWER))
    '''
    外环PID输入角度输出角速度
    et:当前角度误差
    et2:上一次角度误差
    输出：期望角速度
    '''
    def engine_outside_pid(self,et, et2, sum):
        # 输出期望角速度
        palstance = 0.0
        if sum is None:
            # Z轴PID中只做P和D
            palstance = self.kp * et + self.kd * (et - et2)
            palstance = self.engine_limit_palstance(palstance)
            return palstance
        sum[0] += self.ki * et
        # 积分限幅
        sum[0] = self.engine_limit_palstance(sum[0])
        # XY轴PID反馈控制
        palstance = self.kp * et + sum[0] + self.kd * (et - et2)
        # 输出限幅
        palstance = self.engine_limit_palstance(palstance)
        return palstance

    '''
    内环PID输入角速度输出PWM
    et:当前角速度误差
    et2:上一次角速度误差
    输出：PWM调整值
    '''
    def engine_inside_pid(self,et, et2, sum):
        # 输出期望PWM值
        pwm = 0.0
        if sum is None:
            pwm = self.v_kp * et + self.v_kd * (et - et2)
            pwm = self.engine_limit_pwm(pwm)
            return pwm
        sum[0] += self.v_ki * et
        sum[0] = self.engine_limit_pwm(sum[0])
        pwm = self.v_kp * et + sum[0] + self.v_kd * (et - et2)
        pwm = self.engine_limit_pwm(pwm)
        return pwm

    '''
       飞控核心自平衡算法 计算x,y,z三个向量上得PWM调整幅度，
       输入：指令队列_1553a （移除）
             传感器数据队列_1553b
       输出：无
    '''
    def calculate(self,_1553b):
        # GY-99传感器测量的当前角度
        x = int(_1553b.get('ROLL', 0))  #横滚角 X  -180~+180
        y = int(_1553b.get('PITCH', 0)) #俯仰角 Y  -90~+90
        z = int(_1553b.get('YAW', 0)) #偏移角 Z    -180~+180

        # GY-99传感器测量的当前角度 + 遥控器得指令角度 = 当前实际角度误差
        x_et = cfg.ROLL_SET - x
        y_et = cfg.PITCH_SET - y
        z_et = cfg.YAW_SET  - z

        # 传感器测量的当前角速度
        xv = int(_1553b.get('GYRO_X', 0))
        yv = int(_1553b.get('GYRO_Y', 0))
        zv = int(_1553b.get('GYRO_Z', 0))

        # 外环PID根据欧拉角计算出期望角速度
        # 这里应该是期望角度 - 当前实际角度，所以这里为 0 - x_et
        xv_et = self.engine_outside_pid(x_et, self.x_last, self.x_sum)
        yv_et = self.engine_outside_pid(y_et, self.y_last, self.y_sum)
        zv_et = self.engine_outside_pid(z_et, self.z_last, None)
        # print(y_et,self.y_last,self.y_sum,yv_et)

        # 内环输入调整：实际期望角速度 = 期望角速度 - 当前角速度 （补偿当前角速度）
        xv_et -= xv
        yv_et -= yv
        zv_et -= zv

        # 内环PID根据角速度误差计算出PWM调整量
        x_pwm = self.engine_inside_pid(xv_et, self.xv_last, self.xv_sum)
        y_pwm = self.engine_inside_pid(yv_et, self.yv_last, self.yv_sum)
        z_pwm = self.engine_inside_pid(zv_et, self.zv_last, None)
        #print("----------------------------yv=%f,et=%f,et2=%f,sum=%f,pwm=%f" % (yv, yv_et, self.yv_last, self.yv_sum[0], y_pwm))

        # 记录欧拉角的上一次读数
        self.x_last = x_et
        self.y_last = y_et
        self.z_last = z_et

        # 记录角速度的上一次读数
        self.xv_last = xv_et
        self.yv_last = yv_et
        self.zv_last = zv_et

        self.set_power(x_pwm, y_pwm, z_pwm)
        return

