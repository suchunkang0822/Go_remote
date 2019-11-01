from GameBoard import GameBoard
# from Go import Go


class GoRuleChecker:
    FIRST_MOVE = "B"

    def __init__(self):
        pass

    # Already Managed in Board
    # Rule1: game is between two people b and w
    # Rule2: go is played on 19x19 board
    # Rule3: each player has unlimited stones
    # Rule4: Each intersection is either empty or has a valid stone
    # Rule5: Board is empty at beginning

    def checkThatMoveIsValid(self, color, location, boards):
        self.firstMove(color, boards)
        # self.checkBoards(boards)
        # print(len(boards))
        self.checkRule7A(color, location, boards[0])
        # self.checkRule8(color, location, boards)
        self.checkRule8Again(color, location, boards)
        # self.goesTwice(boards, color)
        self.checkGameOver(boards)
        # check that move does not result in repeat
        # check that move does not cause removal of own stones

    def checkOneMove(self, color, location, board):
        self.checkRule7A(color, location, board)

    def checkBoards(self, boards):
        if len(boards) != 3:
            currBoard = GameBoard(boards[0])
            if sum(currBoard.getScore().values()) != len(boards) - 1:
                raise ValueError
        return True

    def goesTwice(self, boards, player):
        diff = []
        if len(boards) > 1:
            for index, row in enumerate(boards[0]):
                diff += [item for item in boards[0][index] if item not in boards[1][index]]
            # print(diff)
            if player in diff:
                raise ValueError

    # Rule6: Black moves first
    def firstMove(self, color, boards):
        if (len(boards) == 1 and color != self.FIRST_MOVE) or (len(boards) == 2 and color == self.FIRST_MOVE):
            raise ValueError
        else:
            return True

    # Rule7: Player may move by saying pass or doing all steps of a move
    # Move Step1: place a stone on empty intersection
    # Can not repeat previous move
    # Move Step2: Remove all opponents that have no liberties
    # Move Step3: Remove all own stones with no liberties

    def checkRule7A(self, player, point, board):
        if player == "W":
            opponent = "B"
        else:
            opponent = "W"

        tempBoard = GameBoard(board)

        tempBoard.insertPiece(point, player)

        neighbors = point.getNeighborPositions()
        # print(point.toString(neighbors))

        for neighbor in neighbors:
            # print(neighbor)
            if tempBoard.locationContains(neighbor) == opponent:
                connected, _ = tempBoard.findAllConnectedNodes(neighbor)
                if tempBoard.canBeReached(neighbor, " "):
                    # has a liberty
                    pass
                else:
                    for node in connected:
                        tempBoard.removePiece(opponent, node)

        connected,_ = tempBoard.findAllConnectedNodes(point)
        if tempBoard.canBeReached(point, " "):
            # has a liberty
            pass
        else:
            if len(connected) > 0:
                raise ValueError

    # Rule8: One may not play in such a way to recreate the board position following on's previous move
    # def checkRule8(self, color, location, boards):
    #     currBoard = GameBoard(boards[0])
    #     if len(boards) > 1:
    #         pastBoard = GameBoard(boards[1])
    #
    #         currCount = currBoard.getScore()[color]
    #         pastCount = pastBoard.getScore()[color]
    #         if (pastBoard.locationContains(location) == color) and (pastCount == currCount + 1):
    #             # print(len(boards))
    #             raise ValueError
    #         else:
    #             return True
    #     return True

    def checkRule8Again(self, color, location, boards):
        # print(boards[0])
        tempBoard = GameBoard(boards[0])

        if tempBoard.insertPiece(location, color) == "This seat is taken!":
            return True

        if tempBoard == boards[-1]:
            raise ValueError

    # Rule9: The game ends when both players have passed consecutively
    def checkGameOver(self, boards):
        if len(boards) == 3 and (boards[0] == boards[1] and boards[1] == boards[2]):
            raise ValueError
        else:
            return True

    # Rule10: The person with more points wins
    def checkBoardValidity(self, boards, player):
        if player == GameBoard().getAcceptedColors()[0]:
            opponent = GameBoard().getAcceptedColors()[1]
        else:
            opponent = GameBoard().getAcceptedColors()[0]

        # print(boards)
        # print(player)
        if len(boards) == 1:
            if player != "B":
                raise ValueError("Invalid start player")
        elif len(boards) == 2:
            if GameBoard(boards[1]).getScore()["B"] != 0 or GameBoard(boards[1]).getScore()["W"] != 0:
                raise ValueError("Need more moves")
            if GameBoard(boards[0]).getScore()["B"] != 1 or GameBoard(boards[0]).getScore()["W"] != 0:
                raise ValueError("Wrong initial move")
            if player != "W":
                raise ValueError("Wrong player value")
        elif len(boards) == 3:
            move1 = self.getMove(boards[1:])
            move2 = self.getMove(boards[:2])

            if move1 == move2 or move2 == player or move1 == opponent:
                # print(move1)
                # print(move2)
                # print("Cannot duplicate moves in any circumstance")
                raise ValueError("Cannot duplicate moves in any circumstance")

            self.checkMoveValidity(move1, boards[1:])
            self.checkMoveValidity(move2, boards[:2])

    def getMove(self, boards):
        for color in GameBoard().getAcceptedColors():
            if GameBoard(boards[1]).getScore()[color] < GameBoard(boards[0]).getScore()[color]:
                return color
        return "pass"

    def checkMoveValidity(self, moveColor, boards):
        difference = GameBoard().subtract(boards[0], boards[1])

        organizedDifference = []
        for color in GameBoard().getAcceptedColors():
            if difference:
                organizedDifference = [pt for pt in difference if pt["Color"] == color]


        for color in organizedDifference:
            if len(color) == 0:
                # move is color[0]["Point"] and color[0]["Color"]
                # execute move on board[1] and see if it equals board[0]
                # if not, those are invalid moves ....
                # if so, valid move

                go = Go(boards[1])

                # Will throw if invalid move
                go.move(color[0]["Color"], color[0]["Point"], boards)
                if go.board != boards[0]:
                    raise ValueError("Not a real move -- does not match simulated move")





