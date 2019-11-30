from FrontEnd import *
import BackEnd
from Go_Board import *
from GoRuleChecker import *
import copy

class Referee:
    def __init__(self):
        self.playerOne = None
        self.playerOneName = None
        self.playerOneStone = "B"
        self.playerTwo = None
        self.playerTwoName = None
        self.playerTwoStone = "W"
        self.boardSize = Go_Board().Board_Size
        # self.board = [[" " for col in range(self.boardSize)] for row in range(self.boardSize)]
        # self.Go_Board = Go_Board(self.board)
        self.boardHistory = [[[" " for col in range(self.boardSize)] for row in range(self.boardSize)]]
        self.current = None
        self.turn = self.playerOneStone
    
    def play_game(self, player1, player2):
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
        while True:
            a = self.playerOneName if self.current == player1 else self.playerTwoName
            #print('im in with',a)
            #print('score',GoRuleChecker().check_the_score(self.boardHistory[0]))
            move = self.current.make_a_move(self.boardHistory)
            #print('this is move inside play of ref',move)
            if move == "This history makes no sense!" or move == "This seat is taken!":
                opponent = self.playerTwoStone if self.current == player1 else self.playerOneStone
                #print('opponent',opponent)
                return self.get_player_name(opponent)
            else:
                winner = self.handleMove(move, self.turn)
                #print('maybe here',winner)
                if winner:
                    return winner
            self.switch_player()
            
    
    def switch_player(self):
        if self.current == self.playerOne:
            self.current = self.playerTwo
            self.turn = self.playerTwoStone
        elif self.current == self.playerTwo:
            self.current = self.playerOne
            self.turn = self.playerOneStone
        
    def assignPlayerOne(self, string):
        self.playerOneName = string

    def assignPlayerTwo(self, string):
        self.playerTwoName = string

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
            return [self.playerOneName]
        else:
            return [self.playerTwoName]

    def decide_winner(self, board):
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


    def get_history(self):
        return self.boardHistory
        
    def handleMove(self, move, player_color):
        # results = []
        # self.boardHistory.append(copy.deepcopy(self.board))
        opponent = "B" if player_color == "W" else "W"
        if move == "pass":
            try:
                self.updateHistory(self.boardHistory[0])
                GoRuleChecker(self.boardHistory).sixth_resolve_history(player_color)
                # self.is_valid_pass(self.boardHistory,move,i)
            except Exception:
                # results.append(self.decide_winner(self.boardHistory[0]))
                # return results
                return self.decide_winner(self.boardHistory[0])
            
        elif move != "pass":
            #print('the move is',move)
            row, col = Go_Board().point_parser(move)
            #print('row col after move',row,col)
            try:
                rule_checker = GoRuleChecker(self.boardHistory)
                rule_checker.sixth_resolve_history(player_color,row,col)
            except Exception:
                return self.get_player_name(opponent)
                # results.append(self.get_player_name(opponent))
                # return results
            else:
                new_board = Go_Board(self.boardHistory[0]).place(player_color,row, col)
                if new_board == "This seat is taken!":
                    return self.get_player_name(opponent)
                else:
                    new_board = rule_checker.board_after_remove_captured_stone(new_board,player_color,row,col)
                    self.updateHistory(copy.deepcopy(new_board))

            # return results



    # def handleMoves(self, listOfMoves, player_color):
    #     results = []
    #     self.boardHistory.append(copy.deepcopy(self.board))
    #     for i, move in enumerate(listOfMoves):
    #         results.append(copy.deepcopy(self.boardHistory))
    #         player_color, opponent_color = self.whose_turn(i)
    #         if move == "pass":
    #             try:
    #                 self.updateHistory(self.boardHistory[0])
    #                 self.is_valid_pass(self.boardHistory,move,i)
    #             except Exception:
    #                 results.append(self.decide_winner(self.boardHistory[0]))
    #                 return results
    #             continue
    #         elif move != "pass":
    #             row, col = Go_Board().point_parser(move)
    #             madeMove = GoRuleChecker(self.boardHistory).sixth_resolve_history(player_color,row,col)
    #             is_ko = self.check_ko(player_color,row,col)
    #             if madeMove and not is_ko:
    #                 self.updateHistory(copy.deepcopy(self.Go.getBoard()))
    #             else:
    #                 results.append(self.get_player_name(opponent_color))
    #                 return results
    #     return results



