#!/usr/bin/python3
# coding=utf-8
'''
    数据链路  飞行器端  UDP-CLIENT
'''

import time
import socket
from FlyControl.param import config as cfg

def working(_1553b):
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            server_ipaddr = cfg.IPADDRESS_GS
            server_port = cfg.PORT_GS_DATA

            while True:
                #print(_1553b)
                #每隔0.3秒将_1553b中数据传给地面站
                bytes_1553b = str(_1553b).encode("utf-8")
                sock_client.sendto(bytes_1553b,(server_ipaddr, server_port))
                time.sleep(0.9)

        except Exception as e:
            print(e)
            print("[Data_Link]回传飞行数据时发生异常...")
            #发生故障不能重新发送？
        finally:
            sock_client.close()