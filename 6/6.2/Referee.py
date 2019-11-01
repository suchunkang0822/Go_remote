import handleInput
from GameBoard import GameBoard
from simpleAI1 import AI1
from Go import Go
import json


class Referee:

    def __init__(self):
        self.playerOne = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoStone = "W"

    def assignPlayerOne(self,string):
        self.playerOne = string

    def assignPlayertwo(self,string):
        self.playerTwo = string



