from board import *
from FrontEnd import *
from BackEnd import *
import json
import abc

class Interface(abc.ABC):
    def __init__(self):
        pass

    # @abstractmethod
    # def first_check_players(self,player):
    #     pass
    #
    # @abstractmethod
    # def second_check_board(self,board):
    #     pass
    #
    # @abstractmethod
    # def third_check_stone(self,stone):
    #     pass

    # @abstractmethod
    # def fourth_check_positions(self,x,y):
    #     pass

    # @abstractmethod
    # def fifth_initial_pos(self,boards):
    #     pass
    # @abstractmethod
    # def sixth_black_first(self,stone,boards):
    #     pass
    # @abstractmethod
    # def seventh_move_checker(self,move):
    #     pass
    #
    #
    # @abstractmethod
    # def input_checker(self,point_boards_or_board):
    #     pass


class RuleChecker(Interface):

    def __init__(self):
        super().__init__()
        pass

    def first_check_players(self,player):
        if player not in ("B","W"):
            return False

    def second_check_board(self,board):
        for i,j in enumerate(board):
            if len(j) != 19:
                # raise TypeError("Board should be 19x19")
                return False

    def third_check_stone(self,stone):
        if not (isinstance(stone,str) and stone in ("B","W")):
            # raise TypeError("stone should either be \"B\" or \"W\"")
            return False





class Play:

    def __init__(self):
        pass

    def fifth_empty(self,board):
        for i, row in enumerate(board):
            for j, element in enumerate(row):
                if element != " ":
                    # raise TypeError("Starting board should be empty")
                    return False
        return True

    def sixth_check_turns(self,stone,boards,row,col):
        e = End()
        if 0 < len(boards) <= 3:
            if len(boards) == 3:
                board1 = boards[2]
            elif len(boards) == 2:
                board1 = boards[1]
            else:
                board1 = boards[0]
            is_empty_board1 = self.fifth_empty(board1)
            if len(boards) <= 2:
                if is_empty_board1 is False:
                    return False
                else:
                    if len(boards) == 1:
                        if stone == "B" and is_empty_board1 is True:
                            return True
                        else:
                            return False
                    elif len(boards) == 2:
                        board2 = boards[0]
                        w, b = stone_counter(board2)
                        is_empty_board2 = self.fifth_empty(board2)
                        if is_empty_board2 is True and stone == "W":
                            return True
                        elif b == 1 and w == 0 and stone == "W":
                            return True
                        else:
                            return False
            else:
                board2, board3 = boards[1], boards[0]
                is_empty_board2, is_empty_board3 = self.fifth_empty(board2), self.fifth_empty(board3)
                if is_empty_board1 is True:
                    if is_empty_board2 is True:
                        if is_empty_board3 is True:
                            return False
                        else:
                            w, b = stone_counter(board3)
                            if b == 0 and w == 1 and stone == "B":
                                return True
                            else:
                                return False
                    else:
                        w2, b2 = stone_counter(board2)
                        if b2 == 1 or w2 == 1:
                            board2_obj, board3_obj = Board(board2), Board(board3)
                            w3, b3 = stone_counter(board3)
                            if b3 == 1 or (b3 == 1 and w3 == 1):
                                coord_b2, coord_b3 = board2_obj.get_coord("B"), board3_obj.get_coord("B")
                                if coord_b2 == coord_b3 and stone == "B":
                                    return True
                            if w3 == 1 or (b3 == 1 and w3 == 1):
                                coord_w2, coord_w3 = board2_obj.get_coord("W"), board3_obj.get_coord("W")
                                if coord_w2 == coord_w3 and stone == "W":
                                    return True
                            return False
                        else:
                            return False
                else:
                    # checking consecutive passes
                    if self.check_consecutive_passes(boards):
                        return False
                    # checking for captured stones that should have been removed
                    for board in boards:
                        if not (check_liberties(board,"W") and check_liberties(board,"B")):
                            return False
                    # check for KO
                    board4 = self.place_stone(stone, board3, row, col)
                    is_ko_13,is_ko_24 = self.is_ko(board1, board3), self.is_ko(board2,board4)
                    if is_ko_13 or is_ko_24:
                        return False
                    # check for any illegal movement of stones b/w board1 & board2
                    list_coord1_2, list_maybe_stones1_2 = board_difference(board1, board2)
                    are_boards_diff_12 = are_boards_different(board2, list_coord1_2, list_maybe_stones1_2)
                    # check for any illegal movement of stones b/w board2 & board3
                    list_coord2_3, list_maybe_stones2_3 = board_difference(board2, board3)
                    are_boards_diff_23 = are_boards_different(board3, list_coord2_3, list_maybe_stones2_3)
                    # check for correct turn
                    turn = is_turn_correct(stone,list_maybe_stones1_2,list_maybe_stones2_3)
                    # check for suicide
                    suicide = self.is_suicide(board3, stone, row, col)
                    # check for double turn
                    double = is_double_turn(list_maybe_stones1_2,list_maybe_stones2_3)

                    if not double and not are_boards_diff_12 and not are_boards_diff_23 and turn and not suicide:
                        return True
                    else:
                        return False
        else:
            return False

    def is_ko(self,board1,board2):
        for i,row in enumerate(board1):
            for j,element in enumerate(row):
                if element != board2[i][j]:
                    return False
        return True


    def is_suicide(self,board,stone,row,col):
        what_if_board = self.place_stone(stone,board,row,col)
        board_obj = Board(what_if_board)
        chain, reached, reached_coord = board_obj.chain_and_reached(row, col)
        if " " not in reached:
            while reached_coord:
                opp = reached_coord.pop(0)
                chain_opp, reached_opp, _ = board_obj.chain_and_reached(opp[0],opp[1])
                if " " in reached_opp:
                    return True
                reached = [x for x in reached if x not in chain_opp]
            return False
        else:
            return False





    def check_consecutive_passes(self,boards):
        if len(boards) == 3 and (boards[0] == boards[1] and boards[1] == boards[2]): return True

    def place_stone(self,stone,board,row,col):
        copy = [row.copy() for row in board]
        copy[row][col] = stone
        return copy

    def bulk_place_stone(self,stone,board,list_coord):
        for coord in list_coord:
            board[coord[0]][coord[1]] = stone
        return board


    def maybe_capture_stones(self,board,row,col):
        board_obj = Board(board)
        chain, reached,_ = board_obj.chain_and_reached(row,col)
        if " " not in reached:
            board = self.bulk_place_stone(" ",board,chain)
            return board,chain
        else:
            return board,[]

    def play_incomplete(self,board,stone,row,col):
        opponent = "W" if stone == "B" else "B"
        board_obj = Board(board)
        board_obj.place_row_col(stone,row,col)
        opp_stones,my_stones = [],[]
        for coord in board_obj.neighbors[row][col]:
            if board_obj.board[coord[0]][coord[1]] == stone:
                my_stones.append(coord)
            elif board_obj.board[coord[0]][coord[1]] == opponent:
                opp_stones.append(coord)

        for coord in opp_stones:
            board, _ = self.maybe_capture_stones(board,coord[0],coord[1])
        for coord in my_stones:
            board, _ = self.maybe_capture_stones(board,coord[0],coord[1])

        return board

    def is_koish(self,board,row,col):
        if board[row][col] == " ": return None
        neighbor_stones = []











class End:

    def __init__(self):
        pass

    @staticmethod
    def area_counter(board):
        current_board = Board(board)
        black_area,white_area = [],[]
        empty_coord_list = list_of_coord(board, " ")
        while empty_coord_list:
            current_empty_coord = empty_coord_list.pop(0)
            chain,reached,_ = current_board.chain_and_reached(current_empty_coord[0],current_empty_coord[1])
            if "W" in reached and ("B" not in reached):
                for i,coord in enumerate(chain):
                    white_area.append(coord)
            elif "B" in reached and ("W" not in reached):
                for i,coord in enumerate(chain):
                    black_area.append(coord)
            empty_coord_list = [x for x in empty_coord_list if x not in chain]
        return len(white_area),len(black_area)

    def check_the_score(self, board):
        w_s, b_s = stone_counter(board)
        w_a, b_a = self.area_counter(board)
        w, b = w_s + w_a, b_s + b_a
        return {"B": b, "W": w}






class RuleCheckerDriver:

    def __init__(self):
        pass

    def driver(self):
        result = []
        r, f, p, e = RuleChecker(), FrontEnd(), Play(), End()
        json_string = f.input_receiver()
        json_list = list(f.parser(json_string))
        for i,read in enumerate(json_list):
            if len(read) == 19:
                board = read
                result.append(e.check_the_score(board))
            elif len(read) == 2:
                stone, move = read[0], read[1]
                stone_checker(stone)
                if move == "pass":
                    result.append(True)
                elif isinstance(move,list):
                    point, boards = move[0], move[1]
                    row, col = parser_xy(point)
                    coord_checker(row,col)
                    latest_board = boards[0]
                    occupied = is_occupied(latest_board,row,col)
                    if occupied is True:
                        result.append(False)
                    else:
                        result.append(p.sixth_check_turns(stone,boards,row,col))

        return json.dumps(result)


def is_double_turn(list_maybe_stones1,list_maybe_stones2):
    list1_2 = [x for x in list_maybe_stones1 if x != " "]
    list2_3 = [x for x in list_maybe_stones2 if x != " "]
    if list1_2 == list2_3:
        return True
    else:
        return False


def board_difference(board1, board2):
    list_maybe_stone, list_coord = [], []
    for i, row in enumerate(board2):
        for j, element in enumerate(row):
            if board1[i][j] != element:
                list_coord.append([i, j])
                list_maybe_stone.append(element)
    return list_coord, list_maybe_stone


def are_boards_different(board, list_coord,list_maybe_stone):
    if len(list_coord) == 1 or len(list_coord) == 0:
        return False
    else:
        w, b = list_maybe_stone.count("W"), list_maybe_stone.count("B")
        if w > 1 or b > 1 or (w == 1 and b == 1):
            return True
        else:
            board_obj = Board(board)
            # if "B" not in list_maybe_stone or "W" not in list_maybe_stone:
            if not ("B" in list_maybe_stone or "W" in list_maybe_stone):
                return False
            else:
                stone = [x for x in list_maybe_stone if x != " "][0]
            opponent = "W" if stone == "B" else "B"
            empty_space_list = [coord for i, coord in enumerate(list_coord) if list_maybe_stone[i] == " "]
            while empty_space_list:
                current_coord = empty_space_list.pop(0)
                chain,reached,_ = board_obj.chain_and_reached(current_coord[0],current_coord[1])
                if opponent in reached:
                    return True
                else:
                    empty_space_list = [x for x in empty_space_list if x not in chain]
            return False


def is_turn_correct(stone, list_maybe_stone1_2, list_maybe_stone2_3):
    if list_maybe_stone2_3:
        last_turn_stone = [x for x in list_maybe_stone2_3 if x != " "]
        if len(last_turn_stone) == 1 and last_turn_stone[0] != stone:
            return True
    else:
        last_turn_stone = [x for x in list_maybe_stone1_2 if x != " "]
        if len(last_turn_stone) == 1 and last_turn_stone[0] == stone:
            return True
        else:
            return False







def check_liberties(board, stone):
    opponent = "W" if stone == "B" else "B"
    board_obj = Board(board)
    stone_list_coord = list_of_coord(board, stone)
    while stone_list_coord:
        coord = stone_list_coord.pop(0)
        chain, reached, _ = board_obj.chain_and_reached(coord[0], coord[1])
        if " " not in reached and opponent in reached:
            return False
        else:
            stone_list_coord = [x for x in stone_list_coord if x not in chain]
    return True


def list_of_coord(board, maybe_stone):
    result = []
    for i,row in enumerate(board):
        for j,element in enumerate(row):
            if element == maybe_stone:
                result.append([i,j])
    return result


def stone_counter(board):
    w, b = 0, 0
    for i, row in enumerate(board):
        for j,element in enumerate(row):
            if element == "B":
                b += 1
            elif element == "W":
                w += 1
    return w, b



if __name__ == '__main__':
    a = RuleCheckerDriver()
    print(a.driver())








