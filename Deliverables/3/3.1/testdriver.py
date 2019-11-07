import handleInput
from GameBoard import GameBoard
import json

def testOnInputs():
    input = handleInput.getInput()
    answers = []

    for tests in input:
        board = GameBoard(tests[0])
        # print(tests)

        for commands in tests[1::]:
            result = handleInput.handleStatement(board, commands)
            answers.append(result)
    result = json.dumps(answers)
    print(result)
    # return json.dumps(answers)


#result = handleInput.testOnInputs()

if __name__ == "__main__":
    testOnInputs()























def testLocalAgainstOutput(outputFile):
    file = open(outputFile, "w")
    file.write(result)

    print(json.dumps(handleInput.getInputFromFile(outputFile)[0]))

    print("Equal: " + str(result == str(json.dumps(handleInput.getInputFromFile(outputFile)[0])).replace("\n", "").replace("\t", "")))

