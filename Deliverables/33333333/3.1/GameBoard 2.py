
class GameBoard:
    BOARD_SIZE = 19
    ACCEPTED_COLORS = ["B", "W", " "]

    def __init__(self, board=[]):
        # Make a verified board checker

        if board:
            # self.checkForValidBoard(board)
            self.board = board
        else:
            self.board = [[" " for x in range(self.BOARD_SIZE)] for y in range(self.BOARD_SIZE)]

    def insertPiece(self, location, color):
        # Check if anything in place and then insert it by updating board
        self.checkForValidColor(color)
        self.checkForValidLocation(location)

        if self.locationContains(location) != " ":
            return "This seat is taken!"
        else:
            self.insertAtAdjustedIndices(location, color)
            return self.board

    def locationContains(self, location):
        # return either the color piece it contains or " " if no piece exists
        return self.getAtAdjustedIndices(location)

    def isOccupied(self, location):
        if self.locationContains(location) == "B" or self.locationContains(location) == "W":
            return True
        else:
            return False

    def canBeReached(self, location, color):
        # Basically we are seeing if there can be a line drawn from any other color to this location
        # if they are directly adjacent, and same color reply true
        # need to traverse
        self.checkForValidColor(color)
        self.checkForValidLocation(location)

        # reachableColors = [[], [], []]
        # for index, c in enumerate(self.ACCEPTED_COLORS):
        #     if (c != " "):
        _, reachableColors = self.findAllConnectedNodes(location, [], color, [self.locationContains(location)])

        # print(reachableColors)

        # for foundColor in reachableColors:
        #     print(reachableColors)
        if color in reachableColors:
            return True
        return False

    def findAllConnectedNodes(self, location, currentlyVisited, color, reachableColors):
        locationChanges = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        if color in reachableColors:
            return currentlyVisited, reachableColors
        
        for locationChange in locationChanges:
            if 0 < location[0] + locationChange[0] < 19 and 0 < location[1] + locationChange[1] < 19:
                if self.locationContains([location[0] + locationChange[0],location[1] + locationChange[1]]) == self.locationContains(location):
                    if not([location[0] + locationChange[0], location[1] + locationChange[1]] in currentlyVisited):
                        currentlyVisited.append([location[0] + locationChange[0], location[1] + locationChange[1]])
    
                        self.findAllConnectedNodes([location[0] + locationChange[0], location[1] + locationChange[1]], currentlyVisited, color, reachableColors)
                else:
                    if not(self.locationContains([location[0] + locationChange[0],location[1] + locationChange[1]]) in reachableColors):
                        reachableColors.append(self.locationContains([location[0] + locationChange[0],location[1] + locationChange[1]]))
                        
    
        return currentlyVisited, reachableColors
    

    def getPoints(self, color):
        points = []
        for y, rowy in enumerate(self.board):
            for x, position in enumerate(rowy):
                if position == color:
                    points.append(str(x+1)+"-"+str(y+1))

        return sorted(points)


    def removePiece(self, color, location):
        # return specified string if not possible, else remove given place
        self.checkForValidLocation(location)

        if self.locationContains(location) != color:
            return "I am just a board! I cannot remove what is not there!"
        else:
            self.insertAtAdjustedIndices(location, " ")
            return self.board


    # INTERNAL METHODS

    # Game board ranges from 1 - 19
    def insertAtAdjustedIndices(self, location, color):
        self.board[location[1] - 1][location[0] - 1] = color

    def getAtAdjustedIndices(self, location):
        return self.board[location[1] - 1][location[0] - 1]

    def checkForValidColor(self, color):
        if not(color in self.ACCEPTED_COLORS) and color != " ":
            print("That is an invalid color", color)
            raise ValueError

    def checkForValidLocation(self, location):
        arrayLocation = [location[0] - 1, location[1] - 1]
        if arrayLocation[1] < 0 or arrayLocation[1] > 18 or arrayLocation[0] < 0 or arrayLocation[0] > 18:
            print("That location is invalid")
            raise ValueError

    def checkForValidBoard(self, board):
        # check number of contained arrays
        if len(board) != self.BOARD_SIZE:
            raise ValueError("Board is invalid")

        for row in board:
            # check the length of every array in board
            if len(row) != self.BOARD_SIZE:
                raise ValueError("Board is invalid")
            # check that every item is valid
            for y, item in enumerate(row):
                if not (item in self.ACCEPTED_COLORS):
                    raise ValueError("Board is invalid")