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
        #print('2')
        raise ValueError

    def make_a_move(self, boards):
        if self.registered and self.received:
            return self.player.make_a_move(boards)
        raise ValueError



# if __name__ == "__main__":
#     pass