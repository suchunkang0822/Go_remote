import testdriver
import sys

def getInputFromFile(filename):
    jsonInputs = []
    currentObj = ""

    file = open(filename, 'r')

    for line in file:
        currentObj += line
        currentObj = currentObj.lstrip()
        try:
            # print(currentObj)
            currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
            # print(currentObj)
            jsonInputs.append(currentDecodedMessage[0])
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

testdriver.testOnInputs()