from GoRuleChecker import *
from GoBoard import GoBoard
import copy



class Referee:
    def __init__(self):
        self.playerMap = {}
        self.playerOneObj = None
        self.playerOneName = None
        self.playerOneStone = "B"
        self.playerTwoObj = None
        self.playerTwoName = None
        self.playerTwoStone = "W"
        self.boardSize = GoBoard().Board_Size
        self.boardHistory = [[[" " for col in range(self.boardSize)] for row in range(self.boardSize)]]
        self.currentStone = self.playerOneStone
        self.currentObj = self.playerOneObj
        self.opponentName = self.playerTwoName
        self.results = {'winner':[], 'loser':[], 'cheater':[]}

    def assignPlayerOne(self, string):
        self.playerOneName = string

    def assignPlayerTwo(self, string):
        self.playerTwoName = string

    def get_player_name(self, stone):
        if stone == "B":
            return self.playerOneName
        else:
            return self.playerTwoName

    def decide_winner(self, board):
        score = GoRuleChecker().check_the_score(board)
        black_score, white_score = score["B"], score["W"]
        if black_score > white_score:
            self.results['winner'].append(self.playerOneName)
            self.results['loser'].append(self.playerTwoName)
        elif white_score > black_score:
            self.results['winner'].append(self.playerTwoName)
            self.results['loser'].append(self.playerOneName)
        else:
            self.results['winner'].append(self.playerOneName)
            self.results['winner'].append(self.playerTwoName)
        return self.results

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
        #print("switched")

    def setupPlayers(self, p1tup, p2tup):
        try:
            p1name, player1 = p1tup
            p2name, player2 = p2tup
            self.assignPlayerOne(p1name)
            self.assignPlayerTwo(p2name)
            # self.playerTwoName = player2.register()
            
            player1.receive_stones(self.playerOneStone)
            player2.receive_stones(self.playerTwoStone)
            self.playerOneObj = player1
            self.playerTwoObj = player2
            self.playerMap[p1name] = player1
            self.playerMap[p2name] = player2
            self.currentObj = player1
            
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
            # TODO: Delete above two lines
            if madeMove:
                whatIfBoard = GoBoard(self.boardHistory[0]).place(self.currentStone,row,col)
                try:
                    self.updateHistory(copy.deepcopy(GoRuleChecker().board_after_remove_captured_stone
                                                     (whatIfBoard,self.currentStone,row,col)))
                except TypeError:
                    self.results['winner'].append(opponentName)
                    self.results['cheater'].append(self.get_player_name(self.currentStone))
                    return self.results
                self.switch_player()
            else:
                self.results['winner'].append(opponentName)
                self.results['cheater'].append(self.get_player_name(self.currentStone))
                return self.results

    def play_game(self,p1tup,p2tup):
        if(self.setupPlayers(p1tup,p2tup)):
            while True:
               
                # move = self.currentObj.make_move(self.boardHistory)
                #print(self.boardHistory[0])
                #print("running: ",move, self.get_player_name(self.currentStone))
                try:
                    move = self.currentObj.make_move(self.boardHistory)
                    results = self.handleMove(move)
                    #print("results", results)
                    if results:
                        # self.switch_player()
                        for winner in results['winner']:
                            response = self.playerMap[winner].end_game()
                            if response != "OK":
                                results['cheater'].append(winner)
                                results['winner'].remove(winner)

                            #print("response:",response)
                        for loser in results['loser']:
                            response = self.playerMap[loser].end_game()
                            if response != "OK":
                                results['cheater'].append(loser)
                                results['loser'].remove(loser)

                        for cheater in results['cheater']:
                            response = self.playerMap[cheater].end_game()
                            if response != "OK":
                                pass
                            #print("response2:",response)
                        # if response1 == "OK":
                        #     if repsonse2 == "OK":

                        return results 
                except TypeError:
                    raise Exception("Game could not be played")
              
