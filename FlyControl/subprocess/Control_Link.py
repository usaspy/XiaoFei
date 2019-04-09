#!/usr/bin/python3
# coding=utf-8
'''
    控制链路  飞行器端  TCP-CLIENT
'''

import time
import socket
from FlyControl.param import config

def working(_1553a):
    while True:
        time.sleep(1)
        print("[Control_Link]正在尝试连接地面站...")
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_ipaddr = config.IPADDRESS_GS
            server_port = config.PORT_GS_CONTROL
            sock_client.connect((server_ipaddr, server_port))

            #飞行控制器从地面站接收控制指令
            print("[Control_Link]已连上地面站...")
            recv_command(sock_client,_1553a)

        except Exception as e:
            del  _1553a[:]
            print("[Control_Link]地面站连接失败，正尝试重连...")
        finally:
            sock_client.close()

#控制链路客户端
#所有命令格式为“CMD:命令字串”
def recv_command(sock,_1553a):
    while True:
        bt = sock.recv(512)
        if bt:
            try:
                _1553a.append(bt)
                print(_1553a)
            except Exception as e:
                print("[Control_Link]命令接收异常！")