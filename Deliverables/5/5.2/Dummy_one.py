from GoRuleChecker import *
from FrontEnd import *
from BackEnd import *
import abc


class Interface(abc.ABC):
    def __init__(self):
        pass


class Player(GoRuleChecker,Interface):
    def __init__(self):
        super().__init__()
        self.stone = ""

    @staticmethod
    def register(string):
        if string == "register":
            return "no name"

    def receive_stone(self,stone):
        self.stone = stone

    def make_a_move(self,boards):
        ref = GoRuleChecker(boards)
        recent_board = self.determine_latest_board(ref)
        boards_correct = ref.sixth_resolve_history(self.stone)
        if boards_correct:
            empty_coord = ref.get_coord(recent_board, " ")
            empty_coord = sorted(empty_coord, key=lambda x: x[1])
            while empty_coord:
                current_coord = empty_coord.pop(0)
                row, col = current_coord[0], current_coord[1]
                if ref.sixth_resolve_history(self.stone, row, col):
                    return str(col+1)+"-"+str(row+1)
                try:
                    ref.check_suicide(self.stone,row,col)
                    ref.check_ko(self.stone,row,col)
                except Exception:
                    continue
            return "pass"
        else:
            return "This history makes no sense!"

    def determine_latest_board(self,GoRuleChecker_obj):
        if GoRuleChecker_obj.board3:
            return GoRuleChecker_obj.board3
        elif GoRuleChecker_obj.board2:
            return GoRuleChecker_obj.board2
        else:
            return GoRuleChecker_obj.board1


def driver():
    result_list = []
    dummy_one = Player()
    j_list = abstract_front_end()
    for i,read in enumerate(j_list):
        if len(read) == 1 and read[0] == "register":
            result_list.append(dummy_one.register(read[0]))
        elif len(read) == 2:
            if read[0] == "receive-stones":
                dummy_one.receive_stone(read[1])
            elif read[0] == "make-a-move":
                result_list.append(dummy_one.make_a_move(read[1]))
    return json.dumps(result_list)


if __name__ == '__main__':

    a = driver()
    print(a)