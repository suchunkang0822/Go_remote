from FrontEnd import *
from Go_Board import *
from Referee import *
from Default import *
from StateProxy import *
import copy
import json

class Driver:
    def __init__(self):
        self.ref = Referee()
        self.playerOne = StateProxy(Default())
        self.playerTwo = StateProxy(Default())


    def testOnInputs(self):

        inputs = abstract_front_end()
        output = []

        if isinstance(inputs[0],str):
            self.playerOne.register(inputs[0])
            self.ref.playerOneName = inputs[0]
            # self.ref.assignPlayerOne(inputs[0])
            output.append(self.ref.playerOneStone)
        if isinstance(inputs[1],str):
            self.playerTwo.register(inputs[1])
            self.ref.playerTwoName = inputs[1]
            # self.ref.assignPlayerTwo(inputs[1])
            output.append(self.ref.playerTwoStone)


        for i,move in enumerate(inputs[2:]):
            # print(self.ref.boardHistory)
            # print("\n\n\n\n\n")
            # print('{}th move'.format(i))
            output.append(copy.deepcopy(self.ref.boardHistory))
            winner = self.ref.handleMove(move)
            if winner:
                # print('winner',winner)
                output.append(winner)
                break
        # print(GoRuleChecker(inputs[0]).sixth_resolve_history("B"))



        # for i,n in enumerate(output):
        #     print(n)
        #     print('\n\n\n\n\n')

        # print(json.dumps(output))
        # for i,n in enumerate(output):
        #     print(n)
        # print(output)
        return json.dumps(output)



if __name__ == "__main__":
    # Driver().testOnInputs()
    print(Driver().testOnInputs())
