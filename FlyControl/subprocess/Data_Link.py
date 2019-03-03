#!/usr/bin/python3
# coding=utf-8
'''
    数据链路  飞行器端  UDP-CLIENT
'''

import time
import socket
from FlyControl.param import config

def working(_1553b_data):
        try:
            sock_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            server_ipaddr = config.IPADDRESS_GS
            server_port = config.PORT_GS_DATA
            while True:
                data = generate_data(_1553b_data)
                sock_client.sendto(data,(server_ipaddr, server_port))

        except Exception as e:
            print(e)
            time.sleep(1)
        finally:
            sock_client.close()

#数据链路客户端
#所有数据格式为“data:命令字串”
def generate_data(_1553b_data):
    return "test"