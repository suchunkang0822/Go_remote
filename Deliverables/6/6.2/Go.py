from GameBoard import GameBoard
from GoRules import GoRuleChecker
import copy
import handleInput


class Go:
    def __init__(self, board):
        self.board = GameBoard(board)
        self.ruleChecker = GoRuleChecker()

    def makeMove(self, location, color, boards):
        try:
            self.ruleChecker.checkBoardValidity(boards, color)
        except ValueError:
            print('dafuq')
            return "This history makes no sense!"

        try:
            self.ruleChecker.checkThatMoveIsValid(color, location, boards)

            self.move(location, color, boards[0])
            
            return True
        except ValueError:
            return False

    def move(self, location, color, board):
        if self.board.insertPiece(location, color) == "This seat is taken!":
            raise ValueError
        self.removeAllNecessary(location, "B") if color == "W" else self.removeAllNecessary(location, "W")
        self.removeAllNecessary(location, color)
    
    def getBoard(self):
        return self.board._board


    def getBoardSize(self):
        return self.board.BOARD_SIZE

    def getAcceptedColors(self):
        return self.board.ACCEPTED_COLORS

    def removeAllNecessary(self, location, color):
        neighbors = location.getNeighborPositions()
        for neighbor in neighbors:

            if self.board.locationContains(location) == color:
                connected, _ = self.board.findAllConnectedNodes(neighbor)
                if self.board.canBeReached(neighbor, " "):
                    # has a liberty
                    pass
                else:
                    # print(counter)
                    # print("heyyyyyyyyyyyyyyyyyyyyyyyy")
                    for node in connected:
                        # print('node',node)
                        # print(self.board._board)
                        # self.board.removePiece(color, node)
                        self.board._board[node.x][node.y] = " "
                        # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                        # print(self.board._)
                        # print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                    # remove all stones returned from canBeReached

    def getFormattedLocation(self, locationString):
        try:
            locationArray = locationString.split("-")
            if len(locationArray) != 2:
                print(locationString + " is not a valid location")
                raise ValueError

            return [int(locationArray[0]) - 1, int(locationArray[1]) - 1]
        except ValueError:
            raise ValueError

    # def handleStatement(board, input):
    #     validActions = ["occupies?", "occupied?", "reachable?", "place", "remove", "get-points"]
    #     if input[0] not in validActions:
    #         return False
    #     if input[0] == "place":
    #         return board.insertPiece(self.getFormattedLocation(input[2]), input[1])
    #     elif input[0] == "remove":
    #         return board.removePiece(input[1], self.getFormattedLocation(input[2]))
    #     elif input[0] == "get-points":
    #         return board.getPoints(input[1])
    #     elif input[0] == "occupies?":
    #         return board.locationContains(getFormattedLocation(input[2])) == input[1]
    #     elif input[0] == "occupied?":
    #         return board.isOccupied(getFormattedLocation(input[1]))
    #     elif input[0] == "reachable?":
    #         return board.canBeReached(getFormattedLocation(input[1]), input[2])
