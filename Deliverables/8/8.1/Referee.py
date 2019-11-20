from FrontEnd import *
import BackEnd
from Go_Board import *
from GoRuleChecker import *
import copy

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
        self.Go_Board = Go_Board(self.board)
        # self.boardHistory = [self.board._board]
        self.boardHistory = []





    def assignPlayerOne(self, string):
        self.playerOne = string

    def assignPlayerTwo(self, string):
        self.playerTwo = string

    def updateHistory(self, board):
        self.boardHistory.insert(0, board)
        if len(self.boardHistory) > 3:
            self.boardHistory.pop()

    def whose_turn(self, number):
        if number % 2 == 0:
            return self.playerOneStone, self.playerTwoStone
        else:
            return self.playerTwoStone, self.playerOneStone

    def get_player_name(self, stone):
        if stone == "B":
            return [self.playerOne]
        else:
            return [self.playerTwo]

    def whose_the_winner(self, board):
        score = GoRuleChecker().check_the_score(board)
        black_score, white_score = score["B"], score["W"]
        if black_score > white_score:
            return [self.playerOne]
        elif white_score > black_score:
            return [self.playerTwo]
        else:
            return sorted([self.playerOne, self.playerTwo])

    def check_ko(self,color,row,col):
        if len(self.boardHistory) == 3:
            try:
                GoRuleChecker(self.boardHistory).check_ko(color,row,col)
            except Exception:
                return False
            else:
                return True

    def is_valid_pass(self,boards,move,nth_turn):
        if len(boards) >= 2 and nth_turn >= 2 or (move == "pass"):
            GoRuleChecker(boards).check_consecutive_passes()


    def handleMoves(self, listOfMoves):
        results = []
        self.boardHistory.append(copy.deepcopy(self.board))
        for i, move in enumerate(listOfMoves):
            results.append(copy.deepcopy(self.boardHistory))
            player_color, opponent_color = self.whose_turn(i)
            if move == "pass":
                try:
                    self.updateHistory(self.boardHistory[0])
                    self.is_valid_pass(self.boardHistory,move,i)
                except Exception:
                    results.append(self.whose_the_winner(self.boardHistory[0]))
                    return results
                continue
            elif move != "pass":
                row, col = Go_Board().point_parser(move)
                madeMove = GoRuleChecker(self.boardHistory).sixth_resolve_history(player_color,row,col)
                is_ko = self.check_ko(player_color,row,col)
                if madeMove and not is_ko:
                    self.updateHistory(copy.deepcopy(self.Go.getBoard()))
                else:
                    results.append(self.get_player_name(opponent_color))
                    return results
        return results

