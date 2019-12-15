
from CustomExceptions import *

class StateProxy:
    def __init__(self, player):
        self.player = player
        self.registered = False
        self.received = False

    def register(self):
        if not self.registered and not self.received:
            self.registered = True
            return self.player.register()
        raise RegisterError('You can not register this player. The player has already been registered')

    def receive_stones(self, stone):
        if self.registered and not self.received:
            self.received = True
            return self.player.receive_stones(stone)
        raise ReceiveStonesError('The player can not receive a stone. The player has already received a stone')

    def make_a_move(self, boards):
        if self.registered and self.received:
            return self.player.make_a_move(boards)
        raise MakeAMoveError('The player can not make a move. The player has not been registered and given a stone')

    def end_game(self):
        if self.registered and self.received:
            response = self.player.end_game()
            self.received = False
            return response
        raise EndGameError('Can not end the game. The player has not been registered nor received a stone')


# class StateProxy:
#     def __init__(self, player):
#         self.player = player
#         self.registered = False
#         self.received = False
#
#     def register(self):
#         if not self.registered and not self.received:
#             self.registered = True
#             return self.player.register()
#         else:
#             raise ValueError
#
#     def receive_stones(self,stone):
#         if self.registered and not self.received:
#             self.received = True
#             return self.player.receive_stones(stone)
#         else:
#             raise ValueError
#
#     def make_a_move(self, boards):
#         if self.registered and self.received:
#             return self.player.make_a_move(boards)
#         raise ValueError
