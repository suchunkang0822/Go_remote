import socket
from FrontEnd import *
HOST = '127.0.0.1'
PORT = 8000


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))
    s.listen()
    conn,addr = s.accept()
    with conn:
        print('Connected by',addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            a =data.decode()
            print('data', list(FrontEnd().parser(a))[0][0])
            print('a',a,type(a))
            conn.sendall(data)