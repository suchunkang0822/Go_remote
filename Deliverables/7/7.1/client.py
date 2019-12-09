from FrontEnd import *
from Default import *
import socket
import time

class Client:
    def __init__(self,player):
        # self.HOST = '192.168.1.152'
        # _, self.PORT, _ = self.fetch_config()
        self.HOST, self.PORT, _ = self.fetch_config()
        self.s = None
        self.player = player

    @staticmethod
    def fetch_config():
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    # @staticmethod
    # def receive_all(s):
    #     response = b""
    #     while True:
    #         res = s.recv(1024)
    #         if not res:
    #             break
    #         response += res
    #     return response

    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((self.HOST,self.PORT))
        except:
            time.sleep(2)
            self.connect()



    def receive_and_send(self):
        data = self.s.recv(6000)
        try:
            json_data = json.loads(data.decode())
        except JSONDecodeError:
            return "end of input"
        # try:
        if len(json_data) == 1 and json_data[0] == "register":
            name = self.player.register()
            self.s.sendall(json.dumps(name).encode())
        elif len(json_data) == 2 and json_data[0] == "receive-stones":
            stone = json_data[1]
            self.player.receive_stones(stone)
        elif len(json_data) == 2 and json_data[0]== "make-a-move":
            history = json_data[1]
            move = self.player.make_a_move(history)
            # print('im in make-move',move)
            self.s.sendall(json.dumps(move).encode())
        else:
            self.s.sendall("GO has gone crazy!".encode())
            self.s.close()
        # except ValueError:
        #     self.s.sendall("GO has gone crazy!".encode())
        #     self.s.close()




if __name__ == "__main__":
    # Client(Default()).receive_and_send()
    a = Client(Default())
    a.connect()
    while True:
        if a.receive_and_send() == "end of input":
            a.s.close()
            break





# class Client:
#     def __init__(self):
#         self.HOST = "localhost"
#         self.PORT = 8888
#
#     @staticmethod
#     def receive_all(s):
#         response = b""
#         while True:
#             res = s.recv(1024)
#             if not res:
#                 break
#             response += res
#         return response
#
#     def connnect(self):
#         with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
#             s.connect((self.HOST,self.PORT))
#             s.sendall(FrontEnd().input_receiver().encode())
#             # data = self.receive_all(s)
#             # return data.decode()
#
# if __name__ == "__main__":
#     Client().connnect()