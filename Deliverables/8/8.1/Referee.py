from FrontEnd import FrontEnd
import BackEnd
from Go_Board import *

class Referee:
    def __init__(self):
        self.playerOne = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoStone = "W"
        self.boardSize = Go_Board().Board_Size
        self.board = [[" " for col in range(self.boardSize)] for row in range(self.boardSize)]

        # initializing game
        # self.Go = Go(self.board._board)
        self.Go = Go(self.board)
        # self.boardHistory = [self.board._board]
        self.boardHistory = []