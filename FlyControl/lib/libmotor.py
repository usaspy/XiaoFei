from FlyControl.param import config

#得到指定马达的当前油门值
def get_curr_power(No):
    return config.MOTOR[No]['CURR_POWER']

#设置指定马达的当前油门值
def set_curr_power(No,new_value):
    config.MOTOR[No]['CURR_POWER'] = new_value

#获取指定马达的GPIO号
def get_gpio(No):
    return config.MOTOR[No]['GPIO']

#换算成马达的PWM值 传入电调 油门范围在0%~100%之间
def convert_power(curr_power):
    #输入电调的PWM值
    v = (100 + curr_power)/20
    #由于接了光耦模块，故取反 用100-v
    return 100 - v





