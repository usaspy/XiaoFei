#!/usr/bin/python3
# coding=utf-8
#
'''
  地面站
  主进程
'''
from multiprocessing import Process
from GroundStation.gui import main_gui
#import affinity

if __name__ == "__main__":
    main_gui
        #p1=链接地面站控制链路进程
        #p1 = Process(target=Control_Link.start,args=(),name='p1')

        #p1.daemon = True

        #p1.start()

       # affinity.set_process_affinity_mask(p1.pid, 7L)

        #p1.join()
