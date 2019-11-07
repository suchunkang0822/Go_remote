from GameBoard import GameBoard
import sys
import json

def getInput():
    jsonInputs = []
    currentObj = ""

    for line in sys.stdin:
        currentObj += line
        currentObj = currentObj.lstrip()
        try:
            # print(currentObj)
            # print("PREPARSE" + currentObj)

            currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
            # print("POST PARSE" + currentObj)
            jsonInputs.append(currentDecodedMessage[0])
            # print(currentObj)
            while currentDecodedMessage[1] < len(currentObj):
                currentObj = currentObj[currentDecodedMessage[1] + 1:]
                try:
                    currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
                    jsonInputs.append(currentDecodedMessage[0])
                except ValueError:
                    pass

            currentObj = ""
        except ValueError:
            pass

    return jsonInputs

# write unittests for these!
def getFormattedLocation(locationString):
    try:
        locationArray = locationString.split("-")
        if len(locationArray) != 2:
            print(locationString + " is not a valid location")
            raise ValueError

        return [int(locationArray[0]), int(locationArray[1])]
    except ValueError:
        raise ValueError

def handleStatement(board, input):
    validActions = ["occupies?", "occupied?", "reachable?", "place", "remove", "get-points"]
    if input[0] not in validActions:
        return False
    if input[0] == "place":
        return board.insertPiece(getFormattedLocation(input[2]), input[1])
    elif input[0] == "remove":
        return board.removePiece(input[1], getFormattedLocation(input[2]))
    elif input[0] == "get-points":
        return board.getPoints(input[1])
    elif input[0] == "occupies?":
        return board.locationContains(getFormattedLocation(input[2])) == input[1]
    elif input[0] == "occupied?":
        return board.isOccupied(getFormattedLocation(input[1]))
    elif input[0] == "reachable?":
        return board.canBeReached(getFormattedLocation(input[1]), input[2])


# inputs = getInput()
# testOnInputs()
# print( GameBoard(inputs[0][0]) )