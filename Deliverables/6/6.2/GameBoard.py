import copy
from Point import Point


class GameBoard:
    BOARD_SIZE = 19
    ACCEPTED_COLORS = ["B", "W"]
    EMPTY = " "

    def __init__(self, board=[]):
        # Make a verified board checker

        if board:
            # self.checkForValidBoard(board)
            self._board = copy.deepcopy(board)
        else:
            self._board = [[self.EMPTY for x in range(self.BOARD_SIZE)] for y in range(self.BOARD_SIZE)]

    def insertPiece(self, location, color):
        # Check if anything in place and then insert it by updating board
        self.checkForValidColor(color)
        self.checkForValidLocation(location)

        if self.locationContains(location) != self.EMPTY:
            return "This seat is taken!"
        else:
            self._insertAtAdjustedIndices(location, color)
            return self._board

    def locationContains(self, location):
        if type(location) == type(""):
            location = Point(location)
        return self._getAtAdjustedIndices(location)

    def isOccupied(self, location):
        if self.locationContains(location) in self.ACCEPTED_COLORS:
            return True
        else:
            return False

    def canBeReached(self, location, color):
        # Basically we are seeing if there can be a line drawn from any other color to this location
        # if they are directly adjacent, and same color reply true
        # need to traverse
        self.checkForValidColor(color)
        self.checkForValidLocation(location)

        _, reachableColors = self.findAllConnectedNodes(location)

        if color in reachableColors:
            return True
        return False

    def findAllConnectedNodes(self, location):
        queue = [location]
        pathColor = self.locationContains(location)
        visited = []
        reachable = []

        while queue:
            if len(reachable) == 3:
                return visited, reachable

            currentLocation = queue.pop()

            visited.append(currentLocation)

            if not (self.locationContains(currentLocation) in reachable):
                reachable.append(self.locationContains(currentLocation))

            for neighbors in currentLocation.getNeighborPositions():
                if self.locationContains(neighbors) == pathColor and not (neighbors in visited):
                    queue.append(neighbors)
                    visited.append(neighbors)
                else:
                    if not (self.locationContains(neighbors) in reachable):
                        reachable.append(self.locationContains(neighbors))

        return visited, reachable

    def findAllConnectedNodesWithEmptyLocations(self, location):
        queue = [location]
        pathColor = self.locationContains(location)
        visited = []
        reachable = []
        empty = []

        while queue:
            currentLocation = queue.pop()

            visited.append(currentLocation)

            # print(currentLocation)

            if self.locationContains(currentLocation) == self.EMPTY:
                empty.append(currentLocation)
                # print(currentLocation)

            for neighbors in currentLocation.getNeighborPositions():
                if self.locationContains(neighbors) == pathColor and not (neighbors in visited):
                    queue.append(neighbors)
                    visited.append(neighbors)
                elif self.locationContains(neighbors) == self.EMPTY:
                    empty.append(neighbors)

        return visited, empty

    def getAllCaptureSpots(self, color, captureSize):
        pastVisited = []
        capturable = []

        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if not(Point([x, y]) in pastVisited) and self.locationContains(Point([x, y])) == color:
                    visited, empty = self.findAllConnectedNodesWithEmptyLocations(Point([x, y]))
                    pastVisited += visited

                    if len(empty) <= captureSize:
                        capturable += empty

        return capturable



    def getPoints(self, color):
        points = []
        for y, rowy in enumerate(self._board):
            for x, position in enumerate(rowy):
                if position == color:
                    points.append(str(Point([x, y])))

        return sorted(points)

    def getScore(self):
        scoreDict = {}
        for color in self.ACCEPTED_COLORS:
            if color != self.EMPTY:
                scoreDict[color] = len(self.getPoints(color))

        return scoreDict

    def removePiece(self, color, location):
        self.checkForValidLocation(location)

        if self.locationContains(location) != color:
            return "I am just a board! I cannot remove what is not there!"
        else:
            self._insertAtAdjustedIndices(location, self.EMPTY)
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            # print(self._board)
            # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
            return copy.deepcopy(self._board)

    def calculatePoints(self):
        allPoints = [[], []]

        alreadyVisited = []
        currentVisited = -1

        # start with a randompoint
        for y, rowy in enumerate(self._board):
            for x, pos in enumerate(rowy):
                for index, color in enumerate(self.ACCEPTED_COLORS):
                    if pos == color:
                        allPoints[index].append([x, y])
                if pos == self.EMPTY:
                    for index, visits in enumerate(alreadyVisited):
                        if Point([x, y]) in visits[0]:
                            currentVisited = index
                    if currentVisited == -1:
                        alreadyVisited.append(self.findAllConnectedNodes(Point([y, x])))
                        currentVisited = len(alreadyVisited) - 1

                    if self.ACCEPTED_COLORS[0] in alreadyVisited[currentVisited][1] and self.ACCEPTED_COLORS[1] not in \
                            alreadyVisited[currentVisited][1]:
                        allPoints[0].append(Point([x, y]))
                    elif self.ACCEPTED_COLORS[0] not in alreadyVisited[currentVisited][1] and self.ACCEPTED_COLORS[1] in \
                            alreadyVisited[currentVisited][1]:
                        allPoints[1].append(Point([x, y]))

                    currentVisited = -1

        return {self.ACCEPTED_COLORS[0]: len(allPoints[0]), self.ACCEPTED_COLORS[1]: len(allPoints[1])}

    # INTERNAL METHODS

    def _insertAtAdjustedIndices(self, point, color):
        self._board[point.x][point.y] = color

    def _getAtAdjustedIndices(self, point):
        # print(self._board)
        try:
            self._board[point.x][point.y]
        except IndexError:
            print('point',point)
            print('indices',point.x,point.y)
            print('board length width',len(self._board),len(self._board[0]))
            print(self._board)
        return self._board[point.x][point.y]

    def checkForValidColor(self, color):
        if not (color in self.ACCEPTED_COLORS) and color != self.EMPTY:
            print("That is an invalid color", color)
            raise ValueError

    def checkForValidLocation(self, location):
        if location.x < 0 or location.x > 18 or location.y < 0 or location.y > 18:
            print("That location is invalid")
            raise ValueError

    def __str__(self):
        temp = ""
        for row in self._board:
            temp += "\n["
            for pos in row:
                temp += '"' + pos + '", '
            temp += "]"
        return temp

    def getAcceptedColors(self):
        return self.ACCEPTED_COLORS

    def subtract(self, board1, board2):
        difference = []
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                if board1[x][y] in self.ACCEPTED_COLORS and board1[x][y] != board2[x][y]:
                    difference.append({"Point": Point([x, y]), "Color": board1[x][y]})
                    return difference

