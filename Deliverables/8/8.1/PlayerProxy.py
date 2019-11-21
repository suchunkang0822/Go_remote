from FrontEnd import FrontEnd
from Remote import *
import socket
import json


class Remote(object):
    def __init__(self, Player):
        # self._wrapped = Remote
        self.HOST, self.PORT, _ = self.fetch_config()
        self.registered = None
        self.received = None
        self.s = None
        self.player = Player
        # self.player = Remote() TODO: should we use ths implementation

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def connect(self,data):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.Host, self.Port))
            # s.sendall(json.dumps(data).encode())
            # data = s.recv(6000)
            # return data.decode()

    def receive_and_send(self):
        data = self.s.recv(6000)
        json_data = json.loads(data.decode('utf-8'))
        if len(json_data) == 1 and json_data[0] == "register":
            name = self.player.register()
            self.s.sendall(json.dumps(name).encode())
        elif len(json_data) == 2 and json_data[0] == "receive-stones":
            stone = json_data[1]
            self.player.receive_stone(stone)
        elif len(json_data) == 2 and json_data[0]== "make-move":
            history = json_data[1]
            move = self.player.make_move(history)
            self.s.sendall(json.dumps(move).encode())
        else:
            return "GO has gone crazy!"





    def verify_protocol(self, command):
        if len(command) == 1 and command[0] == "register":
            if not self.registered:
                self.registered = True
            else:
                return "GO has gone crazy!"
        elif len(command) == 2 and command[0] == "receive-stones":
            if self.registered and (not self.received):
                self.received = True
            else:
                return "GO has gone crazy!"
        else:
            if not(self.registered and self.received):
                return "GO has gone crazy!"


if __name__ == '__main__':
    remote_player = Remote(Player())
    # remote_player.verify_protocol(remote_player._wrapped.register())
    remote_player.connect()
    while True:
        remote_player.receive_and_send()

    PlayerProxy(Remote()).connect()