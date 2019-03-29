import tkinter as tk
from tkinter import messagebox
from GroundStation.subprocess import Control_Link
from GroundStation.subprocess import Data_Link
import threading
import GroundStation.vars as vars



def do_job():
    messagebox.showinfo(title='Info', message='等着吧。。')


def usermanual():
    messagebox.showinfo(title='Manual', message='地面站与飞行器建立链接以后，玩家可以使用键盘操纵飞行器：\n'
                                                'W键：前进\n'
                                                'S键：后退\n'
                                                'A键：左滑\n'
                                                'D键：右滑\n'
                                                'O键：加油\n'
                                                'L键：减油\n'
                                                'K键：左转\n'
                                                '; 键：右转\n'
                                                'N键：一键起飞\n'
                                                'M键：紧急降落')

def open_transmitter():
    try:
        vars.transmitter = threading.Thread(target=Control_Link.working, args=())
        vars.transmitter.setDaemon(True)
        vars.transmitter.start()
        vars.but_1.config(text="关闭地面站发射器")
        vars.but_1.config(command=close_transmitter)
        vars.but_3.config(state='normal')
        vars.but_4.config(state='normal')
        vars.but_5.config(state='normal')
        vars.but_6.config(state='normal')
        vars.but_7.config(state='normal')

    except Exception as e:
        print("打开地面站发射器发生异常")
        vars.but_3.config(state='disabled')
        vars.but_4.config(state='disabled')
        vars.but_5.config(state='disabled')
        vars.but_6.config(state='disabled')
        vars.but_7.config(state='disabled')

def close_transmitter():
    vars.but_1.config(text="打开地面站发射器")
    vars.but_1.config(command=open_transmitter)
    vars.but_2.config(state='disabled')
    vars.but_3.config(state='disabled')
    vars.but_4.config(state='disabled')
    vars.but_5.config(state='disabled')
    vars.but_6.config(state='disabled')
    vars.but_7.config(state='disabled')
    vars.label_1.config(text="状态未知;Unknown")

def show_flydata():
    vars.flydataer = threading.Thread(target=Data_Link.working, args=())
    vars.flydataer.setDaemon(True)
    vars.flydataer.start()


def test_motor():
    pass