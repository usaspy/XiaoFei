#!/usr/bin/python3
# coding=utf-8
#
'''
飞行控制系统的启动入口
 主进程
'''
from multiprocessing import Process
from FlyControl import _1553b
from FlyControl import _1553a
from FlyControl import communication
from FlyControl import sensor
#import affinity

if __name__ == "__main__":
    try:
        print("系统开机...")
        #p1=链接地面站控制链路进程
        p1 = Process(target=communication.start,args=(_1553b,_1553a,),name='p1')
        p2 = Process(target=sensor.start,args=(_1553b,),name='p2')

        p1.daemon = True
        p2.daemon = True

        p1.start()
        p2.start()

        #affinity.set_process_affinity_mask(p1.pid, 7L)
        #affinity.set_process_affinity_mask(p2.pid, 7L)

        p1.join()
        p2.join()
        print("开机成功，系统正在运行...")
    except Exception as e:
        print(e)
    finally:
        print("系统停机...")