#!/usr/bin/python3
# coding=utf-8
'''
    控制链路  飞行器端  TCP-CLIENT
'''

import time
import socket
from FlyControl.param import config

def working(_1553b_cmd):
    while True:
        print("[Control_Link]正在尝试连接地面站...")
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_ipaddr = config.IPADDRESS_GS
            server_port = config.PORT_GS_CONTROL
            sock_client.connect((server_ipaddr, server_port))

            #飞行控制器从地面站接收控制指令
            print("[Control_Link]已连上地面站...")
            recv_command(sock_client,_1553b_cmd)

        except Exception as e:
            del  _1553b_cmd[:]
            print(e)
            print("[Control_Link]地面站连接失败，等待1秒后尝试重连...")
            time.sleep(1)
        finally:
            sock_client.close()

#控制链路客户端
#所有命令格式为“CMD:命令字串”
def recv_command(sock,_1553b_cmd):
    while True:
        bt = sock.recv(512)
        if bt:
            try:
                bts = bt.split(b':')
                cmd = bts[1].decode("utf-8")
                _1553b_cmd.append(cmd)
            except Exception as e:
                print(e)
                print("[Control_Link]命令接收异常！")