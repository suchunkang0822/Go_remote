from FrontEnd import *
import socket
import json
import random

class Player:
    Board_size = 9

    def __init__(self):
        self.player_stone = ""


    def random_coord(self):
        row = random.randrange(1,self.Board_size)
        col = random.randrange(1,self.Board_size)
        return row,col

    @staticmethod
    def register():
        return json.dumps("register")


    def receive_stone(self,stone):
        self.player_stone = stone
        return json.dumps(["receive-stones",stone])

    def make_move(self,boards):
        row,col = self.random_coord()
        while boards[0][row][col] != " ":
            row,col = self.random_coord()
        boards[0][row][col] = self.player_stone
        return json.dumps(["make-a-move",boards])

    def strategy_one(self):
        self.register()
        self.receive_stone("B")



# if __name__ == "__main__":
#     pass