#!/usr/bin/python3
# coding=utf-8
'''
    控制链路 地面站端
'''

import time
import socket
import threading
import GroundStation.Information as info

def start():
        print("[Control_Link]打开地面站发射器...等待链接...")
        try:
            sock_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock_server.bind(('0.0.0.0',13130))

            sock_server.listen()
            while True:
                sock, addr = sock_server.accept()
                print("[Control_Link]与飞行器连接成功...%s:%s" % addr)
                t = threading.Thread(target=send_command, args=(sock, addr))
                t.start()
        except Exception as e:
            print(e)
            print("[Control_Link]地面站发射器发生异常，链接已断开...")
        finally:
            info.CONTROL_LINK_CLIENT = "未知"
            info.CONTROL_LINK_STATUS = 0
            sock_server.close()

#控制链路客户端
#所有命令格式为“CMD:命令字串”
def send_command(sock, addr):
    info.CONTROL_LINK_CLIENT = "%s:%s"% addr
    info.CONTROL_LINK_STATUS = 1
    while True:
        #inp = input("请输入命令: \n >>>")
        inp = "hello everyone"
        if inp == "quit":
            break
        else:
            cmd = "%s:%s"%("CMD",inp)
            print(cmd)
            sock.send(cmd.encode("utf-8"))
    info.CONTROL_LINK_CLIENT = "未知"
    info.CONTROL_LINK_STATUS = 0
