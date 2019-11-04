class Point:
    # feed in a point string
    # get formatted point object
    def __init__(self, location):
        if type(location) == type(""):
            try:
                locationArray = location.split("-")
                if len(locationArray) != 2:
                    raise ValueError(location + " is not a valid location")

                self.x = int(locationArray[1]) - 1
                self.y = int(locationArray[0]) - 1

                if self.x < 0 or self.x > 18 or self.y < 0 or self.y > 18:
                    raise ValueError("That location is invalid")

            except ValueError:
                raise ValueError(location + " is not a valid location")
        else:
            self.x = location[0]
            self.y = location[1]

            if self.x < 0 or self.x > 19 or self.y < 0 or self.y > 19:
                raise ValueError("That location is invalid")

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __str__(self):
        return str(self.y + 1) + "-" + str(self.x + 1)

    def toString(self, listOfPoints):
        tempString = ""
        for point in listOfPoints:
            tempString += str(point) + " "
        return tempString

    def getNeighborPositions(self):
        locationChanges = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        neighbors = []

        for locationChange in locationChanges:
            if 0 <= self.x + locationChange[0] < 19 and 0 <= self.y + locationChange[1] < 19:
                newLocation = [self.x + locationChange[0], self.y + locationChange[1]]
                neighbors.append(Point(newLocation))

        return neighbors

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

