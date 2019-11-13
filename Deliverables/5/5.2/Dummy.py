from RuleChecker import *
from Board import *
from FrontEnd import *
from BackEnd import *
import abc


class Interface(abc.ABC):
    def __init__(self):
        pass


class Player(Interface):
    def __init__(self):
        super().__init__()
        self.stone = ""


    @staticmethod
    def register(string):
        if string == "register":
            return "no name"


    def receive_stone(self,stone):
        self.stone = stone



