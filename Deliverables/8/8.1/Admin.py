from Referee import Referee
import socket
import json
from FrontEnd import FrontEnd
from importlib.machinery import SourceFileLoader
from PlayerProxy import PlayerProxy
from Remote import Remote
import sys

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.default_player = SourceFileLoader("Default", self.DEFPATH).load_module().Default()
        self.s = None
        self.conn = None
        # self.remoteName, self.defaultName = "remote", "default"
        # self.remotePlayer, self.defaultPlayer = self.setup_players()

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        conn, addr = self.s.accept()
            # with conn:
            #     while True:
            #         data = conn.recv(6000)
            #         if len(data) < 6000:
            #             break
            # data = conn.recv(6000)
            # decoded_data = data.decode('utf-8')
            # json_list = list(FrontEnd().parser(decoded_data))
            # return json_list
        self.conn = conn

    def send_and_receive(self):
        input = FrontEnd().input_receiver()
        json_data = FrontEnd().parser(input)
        if len(json_data) == 1 and json_data[0] == "register":
            name = self.player.register()
            print(json.dumps(name).encode())
        elif len(json_data) == 2 and json_data[0] == "receive-stones":
            stone = json_data[1]
            self.player.receive_stone(stone)
        elif len(json_data) == 2 and json_data[0]== "make-move":
            history = json_data[1]
            move = self.player.make_move(history)
            print(json.dumps(move).encode())
        else:
            return "GO has gone crazy!"

    def setup_default_player(self):
        player_module = SourceFileLoader("Default", self.DEFPATH).load_module()
        default_player = player_module.Default()
        return default_player




    # def setup_players(self):
    #     remote = Remote()
    #     remoteProxy = PlayerProxy(remote)
    #     default = None
    #     # TODO default player logic
    #
    #     return remoteProxy, default
    
    def play_game(self):
        data = self.receive_data()



        # initialize connection

if __name__ == "__main__":
    Admin().receive_data()
