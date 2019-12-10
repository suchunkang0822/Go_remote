from GoRuleChecker import *
from GoBoard import GoBoard
import copy



class Referee:
    def __init__(self):
        self.playerOneObj = None
        self.playerOneName = "playerOne"
        self.playerOneStone = "B"
        self.playerTwoObj = None
        self.playerTwoName = "playerTwo"
        self.playerTwoStone = "W"
        self.boardSize = GoBoard().Board_Size
        self.boardHistory = [[[" " for col in range(self.boardSize)] for row in range(self.boardSize)]]
        self.currentStone = self.playerOneStone
        self.currentObj = self.playerOneObj
        self.opponentName = self.playerTwoName

    # def assignPlayerOne(self, string):
    #     self.playerOneName = string

    # def assignPlayerTwo(self, string):
    #     self.playerTwoName = string

    def get_player_name(self, stone):
        if stone == "B":
            return [self.playerOneName]
        else:
            return [self.playerTwoName]

    def decide_winner(self, board):
        score = GoRuleChecker().check_the_score(board)
        black_score, white_score = score["B"], score["W"]
        if black_score > white_score:
            return [self.playerOneName]
        elif white_score > black_score:
            return [self.playerTwoName]
        else:
            return sorted([self.playerOneName, self.playerTwoName])

    def updateHistory(self, board):
        self.boardHistory.insert(0, board)
        if len(self.boardHistory) > 3:
            self.boardHistory.pop()

    def switch_player(self):
        if self.currentStone == self.playerOneStone:
            self.currentStone = self.playerTwoStone
            self.currentObj = self.playerTwoObj
            self.opponentName = self.playerTwoName
        elif self.currentStone == self.playerTwoStone:
            self.currentStone = self.playerOneStone
            self.currentObj = self.playerOneObj
            self.opponentName = self.playerOneName

    def setupPlayers(self, player1, player2):
        try:
            # self.assignPlayerOne(player1.register())
            # self.playerOneName = player1.register()
            #print('end')
            # self.assignPlayerTwo(player2.register())
            # self.playerTwoName = player2.register()
            
            player1.receive_stone(self.playerOneStone)
            player2.receive_stone(self.playerTwoStone)
            self.playerOneObj = player1
            self.playerTwoObj = player2
            self.currentObj = player1
            print("Setting up: ", self.playerOneObj)
            return True
        except ValueError:
            return False
            # "GO has gone crazy!"

    def handleMove(self, move):
        if move == "pass":
            self.updateHistory(self.boardHistory[0])
            self.switch_player()
            is_valid = GoRuleChecker(self.boardHistory).sixth_resolve_history(self.currentStone)
            if not is_valid:
                return self.decide_winner(self.boardHistory[0])
        else:
            row, col = GoBoard().point_parser(move)
            madeMove = GoRuleChecker(self.boardHistory).sixth_resolve_history(self.currentStone, row, col)
            opponentStone = self.playerTwoStone if self.currentStone == self.playerOneStone else self.playerOneStone
            opponentName = self.get_player_name(opponentStone)
            if madeMove:
                whatIfBoard = GoBoard(self.boardHistory[0]).place(self.currentStone,row,col)
                try:
                    self.updateHistory(copy.deepcopy(GoRuleChecker().board_after_remove_captured_stone
                                                     (whatIfBoard,self.currentStone,row,col)))
                except TypeError:
                    return opponentName
                self.switch_player()
            else:
                return opponentName

    def play_game(self,player1,player2):
        if(self.setupPlayers(player1,player2)):
            while True:
                print("running")
                move = self.currentObj.make_move(self.boardHistory)
                try:
                    self.handleMove(move)
                except TypeError:
                    return self.opponentName
                self.switch_player()

