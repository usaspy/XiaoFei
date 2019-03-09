#!/usr/bin/python3
# coding=utf-8
'''
    控制链路 地面站端 TCP-SERVER
'''

import time
import socket
import threading
import GroundStation.vars as vars
import pyHook
import pythoncom

def working():
        print("[Control_Link]打开地面站发射器...等待链接...")
        vars.label_1.config(text="[Control_Link]打开地面站发射器,等待连接...")
        try:
            sock_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock_server.bind(('0.0.0.0',13130))

            sock_server.listen()
            while True:
                sock, addr = sock_server.accept()
                print("[Control_Link]与飞行器连接成功...%s:%s" % addr)
                vars.label_1.config(text="[Control_Link]与飞行器连接成功...%s:%s" % addr)
                vars.CONTROL_LINK_CLIENT = "%s:%s" % addr
                vars.CONTROL_LINK_STATUS = 1
                t = threading.Thread(target=send_command, args=(sock, addr))
                t.setDaemon(True)
                t.start()
        except Exception as e:
            vars.label_1.config(text="[Control_Link]地面站发射器发生异常...")
            print("[Control_Link]地面站发射器发生异常...")
        finally:
            vars.CONTROL_LINK_CLIENT = "未知"
            vars.CONTROL_LINK_STATUS = 0
            sock_server.close()

#控制链路服务器端
#所有命令格式为“命令字串”
def send_command(sock, addr):
    hookmanager = pyHook.HookManager()
    def onKeyDown(event):
        sock.send((event.Key).encode("UTF-8"))
        #print(str(event.Key) + ' is pressed')
        return True
    hookmanager.KeyDown = onKeyDown
    hookmanager.HookKeyboard()
    pythoncom.PumpMessages()
