#!/usr/bin/python3
# coding=utf-8
'''
    数据链路 地面站端 UDP-Server
'''

import time
import socket
import threading
import GroundStation.vars as vars

def start():
        print("[Data_Link]打开飞行数据回传链路...")
        try:
            sock_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock_server.bind(('0.0.0.0',13131))

            while True:
                data,addr = sock_server.recvfrom(1024)
                resolve_data(data)
        except Exception as e:
            print(e)
            print("[Data_Link]数据回传链路接收数据时发生异常...")


#数据链路服务端
def resolve_data(data):
    print(data)
