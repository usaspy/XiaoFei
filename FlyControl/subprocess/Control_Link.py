#!/usr/bin/python3
# coding=utf-8
'''
    控制链路  飞机端
'''

import time
import socket
from FlyControl.param import config

def start(_1553b,_1553b_cmd):
    while True:
        print("[Control_Link]正在尝试链接地面站...")
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server_ipaddr = config.IPADDRESS_GS_CONTROL
            server_port = config.PORT_GS_CONTROL
            sock_client.connect((server_ipaddr, server_port))

            #飞行控制器从地面站接收控制指令
            recv_command(sock_client,_1553b_cmd)

            _1553b["p1_status"] = 1
        except Exception as e:
            _1553b["p1_status"] = 0
            del  _1553b_cmd[:]
            print(e)
            print("[Control_Link]地面站链接失败，等待1秒后尝试重连...")
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