from FrontEnd import *
import socket


class Client:
    def __init__(self,host,port):
        self.HOST = host
        self.PORT = port

    @staticmethod
    def receive_all(s):
        response = b""
        while True:
            res = s.recv(1024)
            if not res:
                break
            response += res
        return response

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(FrontEnd().input_receiver().encode())
            data = self.receive_all(s)
            return data.decode()
            # print('Received', repr(data))
            # print(data.decode())


if __name__ == '__main__':
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 8888  # The port used by the server
    print(Client(HOST,PORT).connect())