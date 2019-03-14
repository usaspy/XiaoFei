from multiprocessing import Process
import time

def xxx():
    while True:
        print("1111111111")
        time.sleep(10)

def yyy():
    while True:
        print("2222222")
        time.sleep(10)
if __name__ == "__main__":
    try:
        print("系统开机...")
        #p1链接地面站控制链路进程
        p1 = Process(target=xxx,args=(),name='p1')
        #p2传感器进程
        p2 = Process(target=yyy,args=(),name='p2')

        p1.daemon = False
        p2.daemon = False

        p1.start()
        p2.start()

        #affinity.set_process_affinity_mask(p1.pid, 7L)
        #affinity.set_process_affinity_mask(p2.pid, 7L)

        print("开机成功，系统正在运行...")
    except Exception as e:
        print(e)
    finally:
        print("系统停机...")