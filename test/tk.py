import tkinter as tk


window = tk.Tk()
window.title('XiaoFei无人机遥控地面站')
window.geometry('900x600')

l = tk.Label(window,text="已经连接",
             font=('Arial',10),
             width=25,height=3)
l.pack()

def do_job():
    pass

menubar=tk.Menu(window)
filemenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='New',command=do_job)
filemenu.add_command(label='Open',command=do_job)
filemenu.add_command(label='Save',command=do_job)
filemenu.add_separator()
filemenu.add_command(label='Exit',command=window.quit)

editmenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_command(label='Cut',command=do_job)
editmenu.add_command(label='Copy',command=do_job)
editmenu.add_command(label='Paste',command=do_job)
window.config(menu=menubar)



on_hit = False
def hit_me():
    global on_hit
    if not on_hit:
        on_hit = True
        print("------------------")
    else:
        on_hit = False
    pass

b = tk.Button(window,
              text='打开',
              width=25,height=2,
              command=hit_me)
b.pack()

e = tk.Entry(window,show=None)
e.pack()

e2 = tk.Entry(window,show=None)
e2.pack()

def insertcode():
    s = e.get()
    e2.insert('end',s)

b1 = tk.Button(window,
              text='输入',
              width=25,height=2,
              command=insertcode)
b1.pack()

t = tk.Text(window,height=6)
t.pack()

canvas = tk.Canvas(window, bg='blue',height=200, width=500)
image_file = tk.PhotoImage(file='s3.png')
image = canvas.create_image(0,0, anchor='nw', image=image_file)
canvas.place(x=20,y=10,anchor='nw')

window.mainloop()