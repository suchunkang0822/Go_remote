import handleInput
from GameBoard import GameBoard
from Go import Go
from Referee import *
import json

def testOnInputs():
    
    inputs = handleInput.getInput()
    output = []
    ref = Referee()
    playerOne = inputs.pop(0)
    playerTwo = inputs.pop(0)

    
    for input in inputs:
        if isinstance(input[0],str):
            ref.assignPlayerOne(in)
            output.append("no name")
        elif input[0] == "receive-stones":
            currentColor = input[1]
        elif input[0] == "make-a-move":
            AI = AI1(input[1], currentColor, 4)
            output.append(AI.makeMove())

    print(json.dumps(output))
    return json.dumps(output)


if __name__ == "__main__":
    testOnInputs()

    # inputs = handleInput.getInput()
    #
    # AI = AI1(inputs[4], "B")
    # print(AI.makeMove())