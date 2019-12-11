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
        
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.s = None
        self.t_style, self.n_remote = self.fetch_tournament_details()
        
        self.remote_connections = self.create_connections(self.n_remote)
        self.player_map = self.setup_player_map()
        self.cheaters = []
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
        self.s.listen(self.n_remote)
        for i in range(n):
            conn, _ = self.s.accept()
            connections.append(conn)
        return connections

    def game_start(self, p1tup, p2tup):
        ref = Referee()
        results = ref.play_game(p1tup, p2tup)
        return results

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

                # Game being played
                results = self.game_start((pid1, self.player_map[pid1]), (pid2, self.player_map[pid2])) 
                winner = results['winner']
                loser = results['loser']
                cheater = results['cheater'] 
                if len(winner) == 2:
                    scoreboard[pid1].append(pid2)
                    scoreboard[pid2].append(pid1)
                    # condition for draw
                else:
                    if loser != []:
                        scoreboard[winner[0]].append(loser[0])
                    elif cheater != []:
                        for player in scoreboard[cheater[0]]:
                            scoreboard[player].append(cheater[0])
                        scoreboard[winner[0]].append(cheater[0])

                # TODO: HANDLE MULTIPLE CHEATERS

                

    def single_knockout(self):
        # i think i can just delete the losers from the array??
        player_names = self.player_map.keys()
        scoreboard = list(player_names)
        rankings = {}

        while(len(scoreboard) > 1):
            for i in range(int(len(scoreboard)/2)):
                new_scoreboard = []
                pid1 = scoreboard[0]
                pid2 = scoreboard[-1]
                results = self.game_start((pid1, self.player_map[pid1]), (pid2, self.player_map[pid2]))
                winner = results['winner']
                loser = results['loser']
                cheater = results['cheater'] 
                if len(winner) == 2:
                    winner, loser = self.coin_flip(winner)
                    new_scoreboard.append(winner)
                    scoreboard.remove(winner)
                    scoreboard.remove(loser)
                    
                    # condition for draw
                elif len(winner) == 1:
                    if loser != []:
                        new_scoreboard.append(winner[0])
                        scoreboard.remove(loser[0])

                    elif cheater != []:
                        new_scoreboard.append(winner[0])
                        scoreboard.remove(cheater[0])
                    scoreboard.remove(winner[0])
                    
                
            scoreboard = new_scoreboard
            # TODO: Need to find loser player and delete name from scorebord
            # remove first -> assign to new scorewboard, remove last -> assign to cheaters if needed
    
    def coin_flip(self, player_arr):
        flip = random.choice(player_arr)
        not_flip = player_arr.remove(flip)[0]        
        return flip, not_flip




if __name__ == "__main__":
    TournamentAdmin()
