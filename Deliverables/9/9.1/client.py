from FrontEnd import *
from Default import *
import socket
import time
import json

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

    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((self.HOST,self.PORT))
        except:
            time.sleep(2)
            self.connect()



    def receive_and_send(self):
        data = self.s.recv(6000)
        print('data',data)
        try:
            json_data = json.loads(data.decode())
        except JSONDecodeError:
            self.s.sendall("GO has gone crazy!".encode())
            return
        if len(json_data) == 1 and json_data[0] == "register":
            name = self.player.register()
            self.s.sendall(json.dumps(name).encode())
            print('im in',name)
        elif len(json_data) == 2 and json_data[0] == "receive-stones":
            stone = json_data[1]
            self.player.receive_stones(stone)
        elif len(json_data) == 2 and json_data[0]== "make-a-move":
            history = json_data[1]
            print('this is history',history)
            move = self.player.make_move(history)
            print('this is move',move)
            self.s.sendall(json.dumps(move).encode())
        elif json_data[0] == "end-game":
            self.s.send(json.dumps('OK').encode())
            return "OK"
        else:
            self.s.sendall("GO has gone crazy!".encode())
            # print('hehey')
            # self.s.close()




if __name__ == "__main__":
    a = Client(Default())
    a.connect()
    while True:
        if a.receive_and_send() == "OK":
            a.s.close()
            break

