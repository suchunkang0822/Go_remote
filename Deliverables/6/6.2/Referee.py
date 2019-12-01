from Go_Board import *
from GoRuleChecker import *
import copy

class Referee:
    def __init__(self):
        self.playerOneObj = None
        self.playerOneName = None
        self.playerOneStone = "B"
        self.playerTwoObj = None
        self.playerTwoName = None
        self.playerTwoStone = "W"
        self.boardSize = Go_Board().Board_Size
        self.boardHistory = [[[" " for col in range(self.boardSize)] for row in range(self.boardSize)]]
        self.currentStone = self.playerOneStone
        self.currentObj = None

    def assignPlayerOne(self, string):
        self.playerOneName = string

    def assignPlayerTwo(self, string):
        self.playerTwoName = string


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
        elif self.currentStone == self.playerTwoStone:
            self.currentStone = self.playerOneStone
            self.currentObj = self.playerOneObj


    def registerPlayers(self, player1, player2):
        try:
            # self.assignPlayerOne(player1.register())
            self.playerOneName = player1.register()
            #print('end')
            # self.assignPlayerTwo(player2.register())
            self.playerTwoName = player2.register()
            player1.receive_stone(self.playerOneStone)
            player2.receive_stone(self.playerTwoStone)
            self.playerOne = player1
            self.playerTwo = player2
            self.current = player1
        except ValueError:
            #print('GO has gone crazy!')
            return "GO has gone crazy!"

    def play(self,move):
        pass
        # opponent = "W" if self.currentStone == "B" else "B"

    def handleMove(self, move):
        # ref = GoRuleChecker(self.boardHistory)
        if move == "pass":
            self.updateHistory(self.boardHistory[0])
            self.switch_player()
            is_valid = GoRuleChecker(self.boardHistory).sixth_resolve_history(self.currentStone)

            if not is_valid:
                # print('board and current stone',self.currentStone)
                # print(self.boardHistory)
                # print('\n\n\n\n')
                return self.decide_winner(self.boardHistory[0])
        else:
            row, col = Go_Board().point_parser(move)
            madeMove = GoRuleChecker(self.boardHistory).sixth_resolve_history(self.currentStone, row, col)
            if madeMove:
                whatIfBoard = Go_Board(self.boardHistory[0]).place(self.currentStone,row,col)
                self.updateHistory(copy.deepcopy(GoRuleChecker().board_after_remove_captured_stone
                                                 (whatIfBoard,self.currentStone,row,col)))
                self.switch_player()
            else:
                opponentStone = self.playerTwoStone if self.currentStone == self.playerOneStone else self.playerOneStone
                return self.get_player_name(opponentStone)





