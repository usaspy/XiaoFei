import tkinter as tk
import GroundStation.gui.function as fun
import GroundStation.vars as vars

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
filemenu.add_command(label='打开发射器',command=fun.open_transmitter)
filemenu.add_command(label='关闭发射器',command=fun.close_transmitter)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=window.quit)

editmenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='帮助',menu=editmenu)
editmenu.add_command(label='操控说明',command=fun.usermanual)
window.config(menu=menubar)

#
vars.label_1 = tk.Label(window,text="状态未知;Unknown",
             bg="Gold",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
vars.label_1.place(x=x0,y=y0,anchor='nw')

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
vars.label_2 = tk.Label(window,text="3000",
             anchor="w",
             foreground='blue',
             font=('Arial',12),
             width=100,height=2)
vars.label_2.place(x=offsetX+100,y=offsetY+40,anchor='nw')

l = tk.Label(window,text="PITCH",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+80,anchor='nw')
vars.label_3 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_3.place(x=offsetX+100,y=offsetY+80,anchor='nw')

l = tk.Label(window,text="YAW",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+120,anchor='nw')
vars.label_4 = tk.Label(window,text="3000",
             anchor="w",
             foreground='green',
             font=('Arial',12),
             width=100,height=2)
vars.label_4.place(x=offsetX+100,y=offsetY+120,anchor='nw')

#---气压 高度  温度
l = tk.Label(window,text="气压",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY,anchor='nw')
vars.label_5 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_5.place(x=offsetX+360,y=offsetY,anchor='nw')

l = tk.Label(window,text="温度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+40,anchor='nw')
vars.label_6 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_6.place(x=offsetX+360,y=offsetY+40,anchor='nw')

l = tk.Label(window,text="海拔高度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+80,anchor='nw')
vars.label_7 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_7.place(x=offsetX+360,y=offsetY+80,anchor='nw')

l = tk.Label(window,text="离地高度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+120,anchor='nw')
vars.label_8 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_8.place(x=offsetX+360,y=offsetY+120,anchor='nw')

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
vars.label_9 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_9.place(x=offsetX+100,y=offsetY+200,anchor='nw')

l = tk.Label(window,text="Y轴",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+240,anchor='nw')
vars.label_10 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_10.place(x=offsetX+100,y=offsetY+240,anchor='nw')

l = tk.Label(window,text="Z轴",
             anchor="w",
             font=('Arial',10),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+280,anchor='nw')
vars.label_11 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_11.place(x=offsetX+100,y=offsetY+280,anchor='nw')

l = tk.Label(window,text="传感器校准",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX,y=offsetY+320,anchor='nw')
vars.label_12 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_12.place(x=offsetX+140,y=offsetY+320,anchor='nw')
#---经度、纬度
l = tk.Label(window,text="GPS经度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+160,anchor='nw')
vars.label_13 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_13.place(x=offsetX+360,y=offsetY+160,anchor='nw')

l = tk.Label(window,text="GPS纬度",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+200,anchor='nw')
vars.label_14 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_14.place(x=offsetX+360,y=offsetY+200,anchor='nw')

l = tk.Label(window,text="飞行时间",
             anchor="w",
             font=('Arial',14),
             width=100,height=2)
l.place(x=offsetX+240,y=offsetY+240,anchor='nw')
vars.label_15 = tk.Label(window,text="3000",
             anchor="w",
             foreground='red',
             font=('Arial',12),
             width=100,height=2)
vars.label_15.place(x=offsetX+360,y=offsetY+240,anchor='nw')
#-----------------
offsetY=50
vars.but_1 = tk.Button(window,
    text='打开地面站发射器',
    activeforeground='red',
    width=25, height=2,
    command=fun.open_transmitter)
vars.but_1.place(x=offsetX+540,y=offsetY,anchor='nw')

vars.but_2 = tk.Button(window,
    text='显示飞行数据',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.show_flydata)
vars.but_2.place(x=offsetX+540,y=offsetY+50,anchor='nw')

vars.but_3 = tk.Button(window,
    text='显示实时图像',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.do_job())
vars.but_3.place(x=offsetX+540,y=offsetY+100,anchor='nw')

vars.but_4 = tk.Button(window,
    text='一键起飞',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.do_job())
vars.but_4.place(x=offsetX+540,y=offsetY+150,anchor='nw')

vars.but_5 = tk.Button(window,
    text='紧急降落',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.do_job())
vars.but_5.place(x=offsetX+540,y=offsetY+200,anchor='nw')

vars.but_6 = tk.Button(window,
    text='传感器校准',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.do_job())
vars.but_6.place(x=offsetX+540,y=offsetY+250,anchor='nw')

vars.but_7 = tk.Button(window,
    text='转速测试',
    activeforeground='red',
    state='disabled',
    width=25, height=2,
    command=fun.do_job())
vars.but_7.place(x=offsetX+540,y=offsetY+300,anchor='nw')
window.mainloop()