import sys
import json

# Given a file as stdin or a series of values entered in stdin
# This function parses it and adds it to an array of json values
# returns array of json values


def getInput():
    jsonInputs = []
    currentObj = ""

    for line in sys.stdin:
        currentObj += line
        currentObj = currentObj.lstrip()
        try:
            currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
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
