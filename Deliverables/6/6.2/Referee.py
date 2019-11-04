import handleInput
from GameBoard import GameBoard
from GoRules import GoRuleChecker
from Go import Go
import json


class Referee:

    def __init__(self):
        self.playerOne = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoStone = "W"
        self.ruleChecker = GoRuleChecker()
        self.board = GameBoard()

    def assignPlayerOne(self,string):
        self.playerOne = string

    def assignPlayerTwo(self,string):
        self.playerTwo = string

    def handleMoves(self, listOfMoves):
        moveHistory = []
        




