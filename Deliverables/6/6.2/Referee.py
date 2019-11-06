import handleInput
from GameBoard import GameBoard
# from GoRules import GoRuleChecker
from Point import Point
from Go import *
import copy
import json


class Referee:

    def __init__(self):
        # initializing players
        self.playerOne = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoStone = "W"

        # emptyBoard initialized to start the Go Instance and Board History
        # self.board = GameBoard()
        self.board = [[" " for col in range(19)] for row in range(19)]

        # initializing game
        # self.Go = Go(self.board._board)
        self.Go = Go(self.board)
        # self.boardHistory = [self.board._board]
        self.boardHistory = []
        

    def assignPlayerOne(self,string):
        self.playerOne = string

    def assignPlayerTwo(self,string):
        self.playerTwo = string

    def handleMoves(self, listOfMoves):
        results = []
        self.boardHistory.append(copy.deepcopy(self.board))
        for i, move in enumerate(listOfMoves):
            results.append(copy.deepcopy(self.boardHistory))
            player_color, opponent_color = self.whose_turn(i)
            if move == "pass":
                try:
                    self.updateHistory(self.boardHistory[0])
                    two_passes = self.Go.ruleChecker.checkGameOver(self.boardHistory)
                except ValueError:
                    results.append(self.whose_the_winner(self.boardHistory[0]))
            else:
                point = Point(move)
                madeMove = self.Go.makeMove(point, player_color, self.boardHistory)
                is_ko = self.check_ko(player_color,point,self.boardHistory)
                if madeMove and not is_ko:
                    self.updateHistory(copy.deepcopy(self.Go.getBoard()))
                else:
                    results.append(self.get_player_name(opponent_color))
                    return results
        return results
    
    def updateHistory(self, board):   
        self.boardHistory.insert(0, board)
        if len(self.boardHistory) > 3:
            self.boardHistory.pop()

    def whose_turn(self, number):
        if number % 2 == 0:
            return self.playerOneStone, self.playerTwoStone
        else:
            return self.playerTwoStone, self.playerOneStone

    def get_player_name(self,stone):
        if stone == "B":
            return [self.playerOne]
        else:
            return [self.playerTwo]

    def whose_the_winner(self,board):
        board_obj = GameBoard(board)
        score = board_obj.getScore()
        black_score, white_score = score["B"], score["W"]
        if black_score > white_score:
            return [self.playerOne]
        elif white_score > black_score:
            return [self.playerTwo]
        else:
            return sorted([self.playerOne,self.playerTwo])

    def check_ko(self,color,location,boards):
        if len(boards) == 3:
            board1,board2,board3 = boards[2],boards[1],boards[0]
            temp_board = copy.deepcopy(boards[0])
            temp_board = GameBoard(temp_board).insertPiece(location,color)
            temp_board = Go(temp_board)
            temp_board.removeAllNecessary(location,color)
            temp_board = temp_board.board._board
            if board1 == board3 or temp_board == board2:
                return True
            else:
                return False
        else:
            return False



            


            
        



        




