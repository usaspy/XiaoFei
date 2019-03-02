import tkinter as tk
import GroundStation.gui.function as fun
window =tk.Tk()
window.title('XiaoFei无人机遥控地面站')
window.geometry('800x450')
window.resizable(0,0)

x0=0
y0=0
x1=800
y1=450

#菜单栏-----------
menubar=tk.Menu(window)
filemenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='功能',menu=filemenu)
filemenu.add_command(label='打开发射器',command=fun.do_job)
filemenu.add_command(label='关闭发射器',command=fun.do_job)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=window.quit)

editmenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='帮助',menu=editmenu)
editmenu.add_command(label='操控说明',command=fun.usermanual)
editmenu.add_command(label='关于XiaoFei',command=fun.do_job)
window.config(menu=menubar)

#
l = tk.Label(window,text="   状态",
             bg="Gold",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=x0,y=y0,anchor='nw')

offsetY=40
offsetX=20
#显示欧拉角
l = tk.Label(window,text="欧拉角",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX,y=offsetY,anchor='nw')

l = tk.Label(window,text="ROLL",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+40,anchor='nw')
l = tk.Label(window,text="PITCH",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+80,anchor='nw')
l = tk.Label(window,text="YAW",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+120,anchor='nw')

#---气压 高度  温度
l = tk.Label(window,text="气压",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY,anchor='nw')

l = tk.Label(window,text="温度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+40,anchor='nw')

l = tk.Label(window,text="海拔高度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+80,anchor='nw')

l = tk.Label(window,text="离地高度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+120,anchor='nw')

#显示加速度
l = tk.Label(window,text="加速度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+160,anchor='nw')

l = tk.Label(window,text="X轴",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+200,anchor='nw')
l = tk.Label(window,text="Y轴",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+240,anchor='nw')
l = tk.Label(window,text="Z轴",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+280,anchor='nw')

l = tk.Label(window,text="传感器校准",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+320,anchor='nw')
#---经度、纬度
l = tk.Label(window,text="GPS经度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+160,anchor='nw')

l = tk.Label(window,text="GPS纬度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+200,anchor='nw')


l = tk.Label(window,text="飞行时间",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+240,anchor='nw')

#-----------------
offsetY=50
b = tk.Button(window,
    text='打开地面站发射器',
    activeforeground='red',
    width=25, height=2,
    command=fun.open_transmitter)
b.place(x=offsetX+540,y=offsetY,anchor='nw')

b = tk.Button(window,
    text='显示飞行数据',
    activeforeground='red',
    width=25, height=2,
    command=fun.show_flydata)
b.place(x=offsetX+540,y=offsetY+50,anchor='nw')

b = tk.Button(window,
    text='显示实时图像',
    activeforeground='red',
    width=25, height=2,
    command=fun.do_job())
b.place(x=offsetX+540,y=offsetY+100,anchor='nw')

b = tk.Button(window,
    text='一键起飞',
    activeforeground='red',
    width=25, height=2,
    command=fun.do_job())
b.place(x=offsetX+540,y=offsetY+150,anchor='nw')

b = tk.Button(window,
    text='紧急降落',
    activeforeground='red',
    width=25, height=2,
    command=fun.do_job())
b.place(x=offsetX+540,y=offsetY+200,anchor='nw')

b = tk.Button(window,
    text='传感器校准',
    activeforeground='red',
    width=25, height=2,
    command=fun.do_job())
b.place(x=offsetX+540,y=offsetY+250,anchor='nw')

b = tk.Button(window,
    text='转速测试',
    activeforeground='red',
    width=25, height=2,
    command=fun.do_job())
b.place(x=offsetX+540,y=offsetY+300,anchor='nw')
window.mainloop()