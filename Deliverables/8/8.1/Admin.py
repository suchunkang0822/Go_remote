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
        # self.remoteName, self.defaultName = "remote", "default"
        # self.remotePlayer, self.defaultPlayer = self.setup_players()

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            # with conn:
            #     while True:
            #         data = conn.recv(6000)
            #         if len(data) < 6000:
            #             break
            data = conn.recv(6000)
            decoded_data = data.decode('utf-8')
            json_list = list(FrontEnd().parser(decoded_data))
            return json_list

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
