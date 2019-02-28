import socket

def socket_client():
    try:
        s = socket.socket()
        s.connect(('127.0.0.1',13130))

        while True:
            bt = s.recv(5)
            if bt:
                print(bt.decode("utf-8"))
                print("============")
    except Exception as e:
        print(e)
    finally:
        s.close()


if __name__ == '__main__':
    socket_client()