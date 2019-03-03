#!/usr/bin/python3
# coding=utf-8

from multiprocessing import Manager

m = Manager()
#数据总线 ，用于存放进程间通信的数据，包括 来自传感器的数据和进程控制开关
_1553b_data = m.dict()
#控制指令总线，用list实现FIFO的指令执行队列
_1553b_cmd = m.list()

#控制链路初始状态 关闭
_1553b_data['p1_status'] = 0
_1553b_data['p2_status'] = 0
_1553b_data['p3_status'] = 0