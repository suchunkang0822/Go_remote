from GoRuleChecker import *
from Go_board import *
from FrontEnd import *
import json


class RuleCheckerDriver(GoRuleChecker):

    def __init__(self):
        super().__init__()

    def driver(self):
        result = []
        f = FrontEnd()
        json_string = f.input_receiver()
        json_list = list(f.parser(json_string))
        for i,read in enumerate(json_list):
            if len(read) == 19:
                board = read
                result.append(self.check_the_score(board))
            elif len(read) == 2:
                stone, move = read[0], read[1]
                self.stone_checker(stone)
                if move == "pass":
                    result.append(True)
                elif isinstance(move,list):
                    point, boards = move[0], move[1]
                    row, col = self.point_parser(point)
                    self.coord_checker(row,col)
                    latest_board = boards[0]
                    occupied = Go_Board(latest_board).is_occupied(row,col)
                    if occupied is True:
                        result.append(False)
                    else:
                        result.append(GoRuleChecker(boards).sixth_resolve_history(stone, row, col))

        return json.dumps(result)


if __name__ == '__main__':
    a = RuleCheckerDriver()
    print(a.driver())
