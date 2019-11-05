import handleInput
from GameBoard import GameBoard
from GoRules import GoRuleChecker
from Go import Go
from Point import Point
import json


class Referee:

    def __init__(self):
        # initializing players
        self.playerOne = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoStone = "W"

        # emptyBoard initialized to start the Go Instance and Board History
        self.board = GameBoard()

        # initializing game
        self.Go = Go(self.board._board)
        self.boardHistory = [self.board._board]
        

    def assignPlayerOne(self,string):
        self.playerOne = string

    def assignPlayerTwo(self,string):
        self.playerTwo = string

    def handleMoves(self, listOfMoves):
        results = []
        
        for i, move in enumerate(listOfMoves):
            print('board history: ', self.boardHistory)
            
         
            color = (self.playerOneStone if i%2==0 else self.playerTwoStone)
           
            # if move == "pass":
            #     self.updateHistory(self.boardHistory[0])
            # else:
    
            point = "pass"
            if move != "pass":
                point = Point(move)
            
            madeMove = self.Go.makeMove(point, color ,self.boardHistory)
            if madeMove:
                
                self.updateHistory(self.Go.getBoard())
                results.append(self.boardHistory)

        return results
    
    def updateHistory(self, board):   
        self.boardHistory.insert(0, board)
        if len(self.boardHistory) > 3:
            self.boardHistory.pop()





            


            
        



        




