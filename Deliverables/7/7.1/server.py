import socket
from Player_two import *


HOST = '127.0.0.1'
PORT = 8888


class Server(Player_two):

    def __init__(self):
        super().__init__()

    def receive_data(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,PORT))
            s.listen()
            request =b""
            conn,addr = s.accept()
            with conn:
                # print('Connected by',addr)
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024:
                        break

                decoded_data = request.decode('utf-8')
                json_list = list(FrontEnd().parser(decoded_data))
                result = self.driver(json_list)
                conn.sendall(result.encode())
                s.close()


if __name__ == '__main__':
    Server().receive_data()