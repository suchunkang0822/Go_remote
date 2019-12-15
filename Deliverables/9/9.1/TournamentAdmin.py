from Referee import Referee
import socket
import json
import copy
import random
from FrontEnd import FrontEnd
from importlib.machinery import SourceFileLoader
from RemoteProxy import RemoteProxy
from StateProxy import StateProxy
import sys

class TournamentAdmin:
    
    def __init__(self):
        self.s = None
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.t_style, self.n_remote = self.fetch_tournament_details()
        self.remote_connections = self.create_connections(self.n_remote)
        
       
        
        self.n_default = 0
        
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

    def shutdown(self):
        for c in self.remote_connections:
            c.close()
        self.s.close()


    def fetch_tournament_details(self):
        if len(sys.argv) != 3:
            raise Exception("Incorrect number of arguments")
        
        _, style, n = sys.argv
        if style not in ["--league","--cup"] or not n.isnumeric():
            raise Exception("Arguments are incorrect")
        
        return style, int(n)
    #print

    def setup_player_map(self):
        player_map = dict()
        n_total = self.total_player_count(self.n_remote)
        self.n_default = n_total - self.n_remote

        for c, conn in enumerate(self.remote_connections):


            # if not remote_name:
            if not conn:
                self.n_default += 1
                self.n_remote -= 1
            else:
                remote = StateProxy(RemoteProxy(conn))
                remote_name = remote.register() + str(c)
                player_map[remote_name] = remote
        
        if self.n_default > 0:
            for i in range(self.n_default):
                default = StateProxy(self.setup_default_player())
                default_name = default.register()+str(i) #TODO: name for local players must be unique

                player_map[default_name] = default
        print('this is player mpa', player_map)
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
        
        self.shutdown()
    

    def round_robin(self):
        #scoring will happen using a map of player name and players defeated
        scoreboard = {}
        cheaters = []
        player_names = list(self.player_map.keys())
        for key in player_names:
            scoreboard[key] = []
        
        #print("player names:",player_names)
        for i1 in range(len(player_names)-1):
            for i2 in range(i1+1, len(player_names)):
                if i2 >= len(player_names) or i1 >= len(player_names)-1:
                    continue
                pid1 = player_names[i1]
                pid2 = player_names[i2]
                
                # Game being played
                results = self.game_start((pid1, self.player_map[pid1]), (pid2, self.player_map[pid2])) 
                winner = results['winner']
                loser = results['loser']
                cheater = results['cheater'] 
                if len(winner) == 2:
                    scoreboard[pid1].append(copy.deepcopy(pid2))
                    scoreboard[pid2].append(copy.deepcopy(pid1))
                    # condition for draw
                # else len(winner) == 1:
                elif len(winner) == 1:
                    if loser != []:
                        scoreboard[winner[0]].append(loser[0])
                    if cheater != []:
                        # handling point give-back 
                        for player in scoreboard[cheater[0]]:
                            if player in scoreboard:
                                scoreboard[player].append(cheater[0])
                        scoreboard[winner[0]].append(cheater[0])
                        player_names.remove(cheater[0])
                        del scoreboard[cheater[0]]
                        cheaters.append(cheater[0])

                        # adding default player\
                        default = StateProxy(self.setup_default_player())
                        default_name = default.register()+str(self.n_default)
                        self.n_default += 1
                        player_names.append(default_name)
                        self.player_map[default_name] = default
                        scoreboard[default_name] = []

                else:
                    for c in cheater:
                        for player in scoreboard[c]:
                            if player in scoreboard:
                                scoreboard[player].append(c)
                        player_names.remove(c)
                        del scoreboard[c]
                        cheaters.append(c)

                        # adding default player
                        default = StateProxy(self.setup_default_player())
                        default_name = default.register()+str(self.n_default)
                        self.n_default += 1
                        player_names.append(default_name)
                        self.player_map[default_name] = default
                        scoreboard[default_name] = []
                #print(scoreboard)
        print(self.calculate_rr(scoreboard, cheaters))
        return self.calculate_rr(scoreboard, cheaters)

                

    def single_knockout(self):
        # i think i can just delete the losers from the array??
        player_names = self.player_map.keys()
        scoreboard = list(player_names)
        cheaters = []
        rounds = []
        rounds.append(copy.deepcopy(scoreboard))
        while(len(scoreboard) > 1):
            new_scoreboard = []
            for i in range(int(len(scoreboard)/2)):
                
                pid1 = scoreboard[0]
                pid2 = scoreboard[-1]
                
                results = self.game_start((pid1, self.player_map[pid1]), (pid2, self.player_map[pid2]))
                #print("results:",results)
                winner = results['winner']
                loser = results['loser']
                cheater = results['cheater'] 
                if len(winner) == 2:
                    rand_winner, rand_loser = self.coin_flip(winner)
                    new_scoreboard.append(rand_winner)
                    scoreboard.remove(rand_winner)
                    scoreboard.remove(rand_loser)
                    # condition for draw
                elif len(winner) == 1:
                    if loser != []:
                        new_scoreboard.append(winner[0])
                        scoreboard.remove(loser[0])

                    elif cheater != []:
                        new_scoreboard.append(winner[0])
                        scoreboard.remove(cheater[0])
                        cheaters.append(cheater[0])
                    scoreboard.remove(winner[0])
                else:
                    defaults = []
                    for c in cheater:

                        # adding default player
                        default = StateProxy(self.setup_default_player())
                        default_name = default.register()+str(self.n_default)
                        self.n_default += 1
                        defaults.append(default_name)
                        self.player_map[default_name] = default
                        scoreboard.remove(c)
                    
                    if len(defaults) == 2:
                        rand_winner, rand_loser = self.coin_flip(defaults)
                        new_scoreboard.append(rand_winner)
                        scoreboard.remove(rand_winner)
                        scoreboard.remove(rand_loser)
                    if len(defaults) == 1:
                        new_scoreboard.append(defaults[0])                    
            
            #print("new sb:",new_scoreboard)
            scoreboard = copy.deepcopy(new_scoreboard)
            rounds.append(new_scoreboard)
        rankings = self.calculate_sk(rounds, cheaters)
        print(rankings)
        return rankings
            # TODO: Need to find loser player and delete name from scorebord
            # remove first -> assign to new scorewboard, remove last -> assign to cheaters if needed
    

    def coin_flip(self, player_arr):
        flip = random.choice(player_arr)
        player_arr.remove(flip)
        not_flip = player_arr[0]      
        return flip, not_flip

    def calculate_rr(self, map, cheaters):
        score_map = {}
        for key in map:
            score_map[key] = len(map[key])
        
        rank_map = {}
        for key in score_map:
            score = score_map[key]
            if score in rank_map:
                rank_map[score].append(key)
            else:
                rank_map[score] = [key]

        rank_map[-1] = cheaters
        rankings = {}
        i = 1
        for ind in sorted(rank_map)[::-1]:
            rankings[i] = rank_map[ind]
            i+=1


        return rankings

    def calculate_sk(self, rounds, cheaters):
        rankings = {}

        for arr in rounds:
            for el in arr:
                if el in cheaters:
                    arr.remove(el)

        for i in range( len(rounds)):
            winner = rounds[len(rounds)-1-i]
            rankings[i+1] = copy.deepcopy(winner)
            for arr in rounds:
                for w in winner:
                    if w in arr:   
                        arr.remove(w)
                #print("rounds",rounds, cheaters, rankings)
        
        
        
        rankings[len(rounds)+1] = cheaters
        print(rankings)
        return rankings


if __name__ == "__main__":
    TournamentAdmin()
