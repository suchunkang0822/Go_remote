from Referee import Referee
import socket
import json
import random
from FrontEnd import FrontEnd
from importlib.machinery import SourceFileLoader
from RemoteProxy import RemoteProxy
from StateProxy import StateProxy
import sys

class TournamentAdmin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.s = None
        self.t_style, self.n_remote = self.fetch_tournament_details()
        
        self.remote_connections = self.create_connections(self.n_remote)
        self.player_map = self.setup_player_map()
        # TO START GAME
        self.setup_game(self.t_style)
        # self.conn = self.create_connection()
        # self.default_player = StateProxy(self.setup_default_player())
        # self.remote_player = StateProxy(RemoteProxy(self.conn))

    # For handling cheaters:
    # In round robin
    #     - assign points back to players that lost to them
    #     - 
    # In single knockout: replace 
    #     - replace player with another default player?

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]


    def fetch_tournament_details(self):
        if len(sys.argv) != 3:
            raise("Incorrect number of arguments")
        
        _, style, n = sys.argv
        if style not in ["--league","--cup"] or not n.isnumeric():
            raise("Arguments are incorrect")
        
        return style, int(n)
    

    def setup_player_map(self):
        player_map = dict()
        n_total = self.total_player_count(self.n_remote)
        n_default = n_total - self.n_remote

        for conn in self.remote_connections:
            remote = StateProxy(RemoteProxy(conn))
            
            remote_name = remote.register()
            print(remote.player.name)

            player_map[remote_name] = remote
            print("registered", player_map)
        
        if n_default > 0:
            for i in range(n_default):
                default = StateProxy(self.setup_default_player())
                default_name = default.register()+str(i) #TODO: name for local players must be unique

                player_map[default_name] = default

        return player_map      


    def total_player_count(self, remote_count):
        i = 0
        temp = 2**i if remote_count > 2 else 2

        while (temp < remote_count):
            i+=1
            temp = 2**i
        
        return temp


    def create_connections(self, n):
        connections = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        for i in range(n):
            conn, _ = self.s.accept()
            connections.append(conn)

        return connections

            # with conn:
            #     while True:
            #         data = conn.recv(6000)
            #         if len(data) < 6000:
            #             break
            # data = conn.recv(6000)
            # decoded_data = data.decode('utf-8')
            # json_list = list(FrontEnd().parser(decoded_data))
            # return json_list
        

    def game_start(self, player1, player2):
        winner = self.ref.play_game(player1, player2)
        return winner


    def setup_default_player(self):
        player_module = SourceFileLoader("Default", self.DEFPATH).load_module()
        default_player = player_module.Default()
        return default_player



    # GAME PLAYING CODE

    def setup_game(self, t_style):
        if t_style == "--league":
            self.round_robin()
        elif t_style == "--cup":
            self.single_knockout()
    

    def round_robin(self):
        #scoring will happen using a map of player name and players defeated
        scoreboard = {}
        player_names = self.player_map.keys()
        for key in player_names:
            scoreboard[key] = []
        

        for i1 in range(len(player_names)):
            for i2 in range(i1, len(player_names)):
                pid1 = player_names[i1]
                pid2 = player_names[i2]
                self.game_start(self.player_map[pid1], self.player_map[pid2]) 

                # TODO: This must return name of the winner and loser so that it can be added to the map
                #       Maybe can be abstracted to a new function that can be shared with single_knockout

                # if cheater:
                # 
                # scoreboard[winner].append(loser)
                

    def single_knockout(self):
        # i think i can just delete the losers from the array??
        player_names = self.player_map.keys()
        scoreboard = list(player_names)

        while(len(scoreboard) > 1):
            pid1 = scoreboard[0]
            pid2 = scoreboard[-1]
            winner = self.game_start(self.player_map[pid1], self.player_map[pid2])
            break
            # TODO: Need to find loser player and delete name from scorebord
            # remove first -> assign to new scorewboard, remove last -> assign to cheaters if needed
    
    def coin_flip(self, p1name, p2name):
        flip = random.choice([p1name, p2name])
        return flip




if __name__ == "__main__":
    TournamentAdmin()
