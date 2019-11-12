from GoRuleChecker import *
from Go_board import *
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
        boards_correct = ref.sixth_resolve_history(self.stone)
        print('board_correct',boards_correct)
        if boards_correct:
            empty_coord = ref.get_coord(self.board3," ")
            empty_coord = sorted(empty_coord, key=lambda x: x[1])
            while empty_coord:
                current_coord = empty_coord.pop(0)
                row, col = current_coord[0], current_coord[1]
                what_if_board = Go_Board(self.board3).place(self.stone,row,col)
                board4_obj = Go_Board(what_if_board)







                suicide = play.is_suicide(board,self.stone,row,col)
                double_turn, is_ko = False, False
                if len(boards) == 3:
                    board1,board2, board3 = boards[2], boards[1], boards[0]
                    _, list_maybe_stones2_3 = board_difference(board2, board3)
                    _, list_maybe_stones3_4 = board_difference(board3, what_if_board)
                    double_turn = is_double_turn(list_maybe_stones2_3,list_maybe_stones3_4)
                    is_ko = play.check_for_ko(self.stone,boards,row,col)
                chain, reached, reached_coord = board4_obj.chain_and_reached(row, col)
                if not suicide and not double_turn and not is_ko:
                    return str(col+1)+"-"+str(row+1)
                else:
                    empty_coord = [x for x in empty_coord if x not in chain]
        else:
            return "This history makes no sense!"


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