import handleInput
from GameBoard import GameBoard
from Go import Go
from Referee import *
import json

def testOnInputs():
    
    inputs = handleInput.getInput()
    output = []
    ref = Referee()
    # playerOne = inputs.pop(0)
    # playerTwo = inputs.pop(0)
    if isinstance(inputs[0],str):
        ref.assignPlayerOne(inputs[0])
        output.append(ref.playerOneStone)
    if isinstance(inputs[1],str):
        ref.assignPlayerTwo(inputs[1])
        output.append(ref.playerTwoStone)
    
    results = ref.handleMoves(inputs[2:])
    output += results


        

    # print(json.dumps(output))

    print('\n'.join(map(str, output)))
    return json.dumps(output)


if __name__ == "__main__":
    testOnInputs()

    # inputs = handleInput.getInput()
    #
    # AI = AI1(inputs[4], "B")
    # print(AI.makeMove())