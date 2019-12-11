from FrontEnd import *
import socket
import json
import random

class StateProxy:
    def __init__(self, player):
        self.player = player
        self.registered = False
        self.received = False

    def register(self):
        if not self.registered and not self.received:
            self.registered = True
            return self.player.register()
        raise ValueError

    def receive_stone(self, stone):
        if self.registered and not self.received:
            self.received = True
            return self.player.receive_stone(stone)
        raise ValueError

    def make_move(self, boards):
        if self.registered and self.received:
            return self.player.make_move(boards)
        raise ValueError

    def end_game(self):
        if self.registered and self.received:
            response = self.player.end_game()
            self.received = False
            return response



# if __name__ == "__main__":
#     pass