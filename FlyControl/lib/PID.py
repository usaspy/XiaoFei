"""
双环串级PID反馈控制：
                外环输入：欧拉角（X，Y，Z）
                外环输出：期望角速度
                内环输入：期望角速度-当前陀螺仪测量的角速度（X，Y，Z）
                内环输出：PWM信号补偿控制电机
"""
import time

class PID(object):
    def __init__(self,p0=0.0,i0=0.0,d0=0.0,p1=0.0,i1=0.0,d1=0.0):
        self.outer_Kp = p0  #外环比例系数P
        self.outer_Ki = i0  #外环积分系数I
        self.outer_Kd = d0  #外环微分系数D
        self.inner_Kp = p1  #内环比例系数P
        self.inner_Ki = i1  #内环积分系数I
        self.inner_Kd = d1  #内环微分系数D

        self.PTerm0 = 0.0 #外环比例修正
        self.ITerm0 = 0.0 #外环积分修正
        self.DTerm0 = 0.0 #外环微分修正

        self.PTerm1 = 0.0 #内环比例修正
        self.ITerm1 = 0.0 #内环积分修正
        self.DTerm1 = 0.0 #内环微分修正

        self.expect_angle = 0.0 #期望角度  X(ROLL) Y(PITCH) Z(YAW)
        self.expect_gyro = 0.0 #期望角速度 X  Y  Z

        self.last_error_angle = 0.0 #上一次角度误差  X(ROLL) Y(PITCH) Z(YAW)
        self.last_error_gyro = 0.0 #上一次角速度误差 X  Y  Z

        self.sample_time = 0.1 #采用时间（秒），因采样频率为10HZ，故设为0.1
        self.curr_time = time.time()   #当前时间
        self.last_time = self.curr_time

        self.limited_angle_max = 40.0 #角度积分上限
        self.limited_gyro_max = 20.0 #角速度积分上限

        self.outer_output = 0 #外环输出
        self.inner_output = 0 #内环输出

    '''
        双环串级PID算法
        输入：当前欧拉角 当前角速度
        输出：电机PWM值
    '''
    def update(self,curr_angle=0.0,curr_gyro=0.0):
        #1.外环计算期望角速度
        angle_error = self.expect_angle - curr_angle # 外环输入参数       当前角度误差 = 期望角度（自稳时为常量0） - 当前角度
        self.curr_time = time.time()  #设置当前时间
        duration = self.curr_time - self.last_time  # 上次调用到本次调用的时间间隔，积微分用

        if duration >= self.sample_time:
            self.PTerm0 = self.outer_Kp * angle_error  #外环Kp * 当前角度误差
            self.ITerm0 += angle_error * duration #误差积分

            if self.ITerm0 > self.limited_angle_max:
                self.ITerm0 = self.limited_angle_max
            elif self.ITerm0 < -self.limited_angle_max:
                self.ITerm0 = -self.limited_angle_max

        #2.内环计算PWM
        pass