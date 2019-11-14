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
        self.player_stone = ""

    @staticmethod
    def register(string):
        if string == "register":
            return "no name"

    def receive_stone(self,stone):
        self.player_stone = stone

    def make_a_move(self,boards):
        ref = GoRuleChecker(boards)
        recent_board = self.determine_latest_board(ref)
        boards_correct = ref.sixth_resolve_history(self.player_stone)
        if boards_correct:
            capture = self.n_depth_capture(boards,1)
            if capture:
                return capture
            else:
                empty_coord = ref.get_coord(recent_board, " ")
                empty_coord = sorted(empty_coord, key=lambda x: x[1])
                while empty_coord:
                    current_coord = empty_coord.pop(0)
                    row, col = current_coord[0], current_coord[1]
                    if ref.sixth_resolve_history(self.player_stone, row, col):
                        return str(col+1)+"-"+str(row+1)
                    try:
                        ref.check_suicide(self.player_stone,row,col)
                        ref.check_ko(self.player_stone,row,col)
                    except Exception:
                        continue
                return "pass"
        else:
            return "This history makes no sense!"

    @staticmethod
    def determine_latest_board(GoRuleChecker_obj):
        if GoRuleChecker_obj.board3:
            return GoRuleChecker_obj.board3
        elif GoRuleChecker_obj.board2:
            return GoRuleChecker_obj.board2
        else:
            return GoRuleChecker_obj.board1

    def n_depth_capture(self,boards,n = 1):
        opponent = "B" if self.player_stone == "W" else "W"
        ref = GoRuleChecker(boards)
        latest_board = self.determine_latest_board(ref)
        set_of_liberties = ref.check_liberties(latest_board,opponent,"coord")
        if n == 1:
            liberties_one = []
            for i,liberties in enumerate(set_of_liberties):
                if len(liberties) == 1:
                    liberties_one.append(liberties[0])
            if liberties_one:
                liberties_one = sorted(liberties_one, key=lambda x: x[1])
                if ref.sixth_resolve_history(self.player_stone, liberties_one[0][0], liberties_one[0][1]):
                    return str(liberties_one[0][1] + 1) + "-" + str(liberties_one[0][0] + 1)
        # else:
        #     while set_of_liberties:
        #         current_liberties = set_of_liberties.pop(0)






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