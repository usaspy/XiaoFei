import socket
import threading
import time

def socket_server():
    try:
        s = socket.socket()
        s.bind(('127.0.0.1',13130))

        s.listen()
        while True:
            sock,addr = s.accept()
            t = threading.Thread(target=operate,args=(sock,addr))
            t.start()
    except Exception as e:
        print(e)
    finally:
        s.close()


def operate(sock,addr):
    print(sock)
    print(addr)
    while True:
        sock.send("command1".encode("utf-8"))
        sock.send("command2".encode("utf-8"))
        time.sleep(1)

if __name__ == '__main__':
    socket_server()