import tkinter as tk
from tkinter import messagebox

def do_job():
   # messagebox.showinfo(title='Info', message='等着吧。。')
    pass

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