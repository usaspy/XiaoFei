'''
进行PID调试时使用
生成PID输出数据文件（csv格式）
生成PID输出图形
'''
import matplotlib.pyplot as plt
'''
依据数据文件生成Chart曲线图
Y1：
Y2：
X：时间轴
'''

d1= []
d2= []
d3= []
d4= []
x= []

def generate_pid_chart():
    i = 0
    with open('d://data.log', 'r') as f:
        lines = f.readlines()
        for line in lines:
            ls = line.split(',')
            d1.append(int(ls[0]))
            d2.append(int(ls[1]))
            d3.append(int(ls[2]))
            d4.append(int(ls[3]))
            i+=1
            x.append(i)
        print(d1)
    plt.plot(x, d1, 'yo-')
    plt.plot(x, d2, 'go-')
    plt.plot(x, d3, 'bo-')
    plt.plot(x, d4, 'ro-')
    plt.title('test ROLL ')
    plt.grid()
    plt.tight_layout()
    plt.show()


generate_pid_chart()