from Referee import Referee
import socket
import json
from FrontEnd import FrontEnd
from importlib.machinery import SourceFileLoader
from RemoteProxy import RemoteProxy
from StateProxy import StateProxy
import sys

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.s = None
        self.conn = self.create_connection()
        self.default_player = StateProxy(self.setup_default_player())
        self.remote_player = StateProxy(RemoteProxy(self.conn))

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        conn, _ = self.s.accept()
        return conn
            # with conn:
            #     while True:
            #         data = conn.recv(6000)
            #         if len(data) < 6000:
            #             break
            # data = conn.recv(6000)
            # decoded_data = data.decode('utf-8')
            # json_list = list(FrontEnd().parser(decoded_data))
            # return json_list
        

    def game_start(self):
        self.ref.play_game(self.remote_player, self.default_player)

    # def send_and_receive(self):
    #     input = FrontEnd().input_receiver()
    #     json_data = FrontEnd().parser(input)
    #     if len(json_data) == 1 and json_data[0] == "register":
    #         name = self.player.register()
    #         print(json.dumps(name).encode())
    #     elif len(json_data) == 2 and json_data[0] == "receive-stones":
    #         stone = json_data[1]
    #         self.player.receive_stone(stone)
    #     elif len(json_data) == 2 and json_data[0]== "make-move":
    #         history = json_data[1]
    #         move = self.player.make_move(history)
    #         print(json.dumps(move).encode())
    #     else:
    #         return "GO has gone crazy!"

    def setup_default_player(self):
        player_module = SourceFileLoader("Default", self.DEFPATH).load_module()
        default_player = player_module.Default()
        return default_player


        # initialize connection

if __name__ == "__main__":
    Admin().receive_data()
