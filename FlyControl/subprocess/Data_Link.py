#!/usr/bin/python3
# coding=utf-8
'''
    数据链路  飞行器端  UDP-CLIENT
'''

import time
import socket
from FlyControl.param import config

def working(_1553b):
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            server_ipaddr = config.IPADDRESS_GS
            server_port = config.PORT_GS_DATA

            while True:
                #print(_1553b)
                #将_1553b中得数据传给地面站,等待0.2秒？
                sock_client.sendto(str(_1553b).encode("utf-8"),(server_ipaddr, server_port))
                time.sleep(0.3)

        except Exception as e:
            print(e)
            time.sleep(1)
        finally:
            sock_client.close()