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
        results.append(self.boardHistory)
        
        for i, move in enumerate(listOfMoves):
            
            print('board history', self.boardHistory)
            
         
            color = (self.playerOneStone if i%2==0 else self.playerTwoStone)
           
            # if move == "pass":
            #     self.updateHistory(self.boardHistory[0])
            # else:
    
            point = "pass"
            if move != "pass":
                point = Point(move)
            tempHistory = self.boardHistory
            madeMove = self.Go.makeMove(point, color ,tempHistory)
            
            print(madeMove)
            if madeMove:
                results.append(self.boardHistory)
                # print('after board history', self.boardHistory)
                self.updateHistory(self.Go.getBoard())
                print('currboard: ', self.Go.getBoard())
                print('results: ', results)
                
                

        return results
    
    def updateHistory(self, board):   
        self.boardHistory.insert(0, board)
        if len(self.boardHistory) > 3:
            self.boardHistory.pop()





            


            
        



        




