#!/usr/bin/python3
# coding=utf-8
#
'''
飞行控制系统的启动入口
 主进程
'''
from multiprocessing import Process,Lock
from FlyControl import _1553b
from FlyControl import _1553a
from FlyControl import communication
from FlyControl import engine
from FlyControl import sensor
#import affinity
import os

if __name__ == "__main__":
    try:
        print("系统开机...")
        lock = Lock()
        #p1 控制通信进程
        p1 = Process(target=communication.start,args=(_1553b,_1553a,),name='p1')
        #p2 姿态传感器进程
        p2 = Process(target=sensor.start,args=(_1553b,lock,),name='p2')
        #p3 动力引擎进程
        p3 = Process(target=engine.init,args=(_1553b,_1553a,),name='p3')

        p1.daemon = True
        p2.daemon = True
        p3.daemon = True

        p1.start()
        p2.start()
        p3.start()

        #affinity.set_process_affinity_mask(p1.pid, 7L)
        #affinity.set_process_affinity_mask(p2.pid, 7L)
        #affinity.set_process_affinity_mask(p3.pid, 7L)
        #以上方法在python3以后貌似失效了
        #可以用下面的方法来做
        os.sched_setaffinity(p1.pid,[0x00])  #通信进程绑定在CPU-0上执行
        os.sched_setaffinity(p2.pid,[0x01])  #传感器进程绑定在CPU-1上执行
        os.sched_setaffinity(p3.pid,[0x02])  #动力进程绑定在CPU-2上执行
        #其中CPU 0 [1 2] 3 已禁用OS调度策略

        p1.join()
        p2.join()
        p3.join()
    except Exception as e:
        print(e)
    finally:
        print("系统停机...")