from GoBoard import *
from FrontEnd import *
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


class GoRuleChecker(Go_Board, Interface):
    def __init__(self,boards=None):
        super().__init__()
        # self.board_history = self.validate_size_history(boards)
        # self.board1, self.board2, self.board3 = self.assign_boards(boards)
        if boards:
            self.board_history = self.validate_size_history(boards)
            self.board1, self.board2, self.board3 = self.assign_boards(boards)
        else:
            self.board_history, self.board1, self.board2, self.board3 = None, None, None, None

    @staticmethod
    def validate_size_history(boards):
        if len(boards) > 3:
            raise Exception('size of board history is invalid')
        else:
            return boards

    @staticmethod
    def assign_boards(boards):
        if len(boards) == 3:
            return boards[2], boards[1], boards[0]
        elif len(boards) == 2:
            return boards[1], boards[0], False
        elif len(boards) == 1:
            return boards[0], False, False
        else:
            raise Exception('There is no board history')

    #############

    def first_check_players(self,player):
        self.stone_checker(player)

    # second_check_board is automatically run when RuleChecker object is created

    # third_check_stones is a match case with

    ############ Rule 4
    @staticmethod
    def check_liberties(board, stone):
        opponent = "W" if stone == "B" else "B"
        go_board_obj = Go_Board(board)
        list_of_stone_coord = go_board_obj.get_coord(board, stone)
        while list_of_stone_coord:
            coord = list_of_stone_coord.pop(0)
            chain, reached, _ = go_board_obj.chain_and_reached(coord[0], coord[1])
            if " " not in reached and opponent in reached:
                return False
            else:
                list_of_stone_coord = [x for x in list_of_stone_coord if x not in chain]
        return True


    ############
    @staticmethod
    def fifth_is_empty(board):
        for i, row in enumerate(board):
            for j, element in enumerate(row):
                if element != " ":
                    return False
        return True

    ############ Rule 6

    def sixth_resolve_history(self, player, row=None, col=None):
        try:
            self.check_turn(player)
            if len(self.board_history) == 1:
                if self.if_history_one():
                    return True
            elif len(self.board_history) == 2:
                if self.if_history_two():
                    return True
            else:
                if isinstance(row,int) and isinstance(col,int):
                    if self.if_history_three(player,row,col):
                        return True
                else:
                    if self.if_history_three(player):
                        return True
        except Exception:
            return False





    def if_history_one(self):
        if self.fifth_is_empty(self.board1):
            return True
        else:
            # return False
            raise Exception('Board history of length one should be empty')

    def if_history_two(self):
        w2, b2 = self.stone_counter(self.board2)
        if self.if_history_one():
            if (b2 == 1 or b2 == 0) and w2 == 0:
                return True
            else:
                raise Exception('Invalid number of stones in board2')
        else:
            raise Exception('Board history of length two should have board1 empty')

    def if_history_three(self,stone,row=None,col=None):
        w2, b2 = self.stone_counter(self.board2)
        w3, b3 = self.stone_counter(self.board3)
        try:
            if self.fifth_is_empty(self.board1):
                if (b2 == 1 or b2 == 0) and w2 == 0:
                    if b2 ==1:
                        if (w3 == 1 and b3 == 1) or (w3 == 0 and b3 ==1):
                            return True
                        else:
                            raise Exception
                    else:
                        if w3 == 1 and b3 == 0:
                            return True
                        else:
                            raise Exception
                else:
                    if w2 == 1 and b2 == 0:
                        if (w3 == 1 and b3 == 1) or w3 == 1:
                            w2_coord, w3_coord = self.get_coord(self.board2, "W"), self.get_coord(self.board3, "W")
                            if w2_coord == w3_coord:
                                return True
                            else:
                                raise Exception
                        else:
                            raise Exception
                    else:
                        raise Exception
            else:
                if isinstance(row,int) and isinstance(col,int):
                    if self.check_illegal_moves(stone,row,col):
                        return True
                else:
                    if self.check_illegal_moves(stone):
                        return True
        except Exception:
            raise Exception('Board history of length three invalid')

    def check_illegal_moves(self,player,row=None,col=None):
        try:
            if isinstance(row,int) and isinstance(col,int):
                self.check_suicide(player, row, col)
                self.check_ko(player, row, col)
            self.check_ko(player)
            self.check_consecutive_passes()
            self.check_should_remove()
            self.check_board_difference(self.board1,self.board2)
            self.check_board_difference(self.board2,self.board3)
        except Exception:
            raise Exception('There is a problem in the board history')
        else:
            return True

    def check_suicide(self,stone,row,col):
        what_if_board = Go_Board(self.board3).place(stone,row,col)
        board_obj = Go_Board(what_if_board)
        chain, reached, reached_coord = board_obj.chain_and_reached(row, col)
        if " " not in reached:
            while reached_coord:
                opp = reached_coord.pop(0)
                chain_opp, reached_opp, _ = board_obj.chain_and_reached(opp[0],opp[1])
                if " " not in reached_opp:
                    return True
                else:
                    continue
            raise Exception('This move is suicidal')
        else:
            return True

    def check_consecutive_passes(self):
        if self.board1 == self.board2 and self.board2 == self.board3:
            raise Exception('consecutive passes detected')

    def check_should_remove(self):
        for i,board in enumerate(self.board_history):
            if not (self.check_liberties(board,"B") and self.check_liberties(board,"W")):
                raise Exception('zero liberty stone present')

    def check_ko(self,stone,row=None,col=None):
        if self.board1 == self.board3:
            raise Exception('Ko detected')
        elif isinstance(row,int) and isinstance(col,int):
            what_if_board = Go_Board(self.board3).place(stone, row, col)
            if what_if_board != 'This seat is taken!':
                what_if_board = self.board_after_remove_captured_stone(what_if_board, stone, row, col)
                if self.board2 == what_if_board:
                    raise Exception('Ko detected')
                else:
                    return True
            else:
                raise Exception('coordinate occupied')
        else:
            return True

    @staticmethod
    def board_after_remove_captured_stone(what_if_board,player,row,col):
        opponent = "B" if player == "W" else "W"
        board_obj = Go_Board(what_if_board)
        neighbor_list = board_obj.get_valid_neighbors([row,col])
        neighbor_list = sorted(neighbor_list, key=lambda x: x[1])
        while neighbor_list:
            current_coord = neighbor_list.pop(0)
            neighbor_row,neighbor_col = current_coord[0], current_coord[1]
            chain,reached,reached_coord = board_obj.chain_and_reached(neighbor_row,neighbor_col)
            if (" " not in reached) and (opponent not in reached):
                for i,coord in enumerate(chain):
                    board_obj.remove(opponent,coord[0],coord[1],"in_place")
        return board_obj.board



    @staticmethod
    def board_difference(board1,board2):
        list_coord, diffMStones1_2, diffMStones2_1 = [],[],[]
        for i, row in enumerate(board2):
            for j, element in enumerate(row):
                if board1[i][j] != element:
                    list_coord.append([i, j])
                    diffMStones2_1.append(element)
                    diffMStones1_2.append(board1[i][j])
        return list_coord, diffMStones1_2, diffMStones2_1

    def check_board_difference(self,board1,board2):
        list_coord, _, diffMStones2_1 = self.board_difference(board1,board2)
        if len(diffMStones2_1) > 1:
            w2_1,b2_1 = diffMStones2_1.count("W"), diffMStones2_1.count("B")
            if w2_1 + b2_1 > 1:
                raise Exception('more than one stone placed per turn')
            else:
                player = [x for x in diffMStones2_1 if x != " "][0]
                player_coord = list_coord[diffMStones2_1.index(player)]
                player_row,player_col = player_coord[0], player_coord[1]
                if "B" in diffMStones2_1 or "W" in diffMStones2_1:
                    empty_space_list = [coord for i, coord in enumerate(list_coord) if diffMStones2_1[i] == " "]
                    while empty_space_list:
                        current_coord = empty_space_list.pop(0)
                        chain, reached, reach_coord = Go_Board(board1).chain_and_reached(current_coord[0],current_coord[1])
                        if reached.count(" ") == 1:
                            correct_board_2 = Go_Board(board1).place(player,player_row,player_col)
                            correct_board_2 = self.board_after_remove_captured_stone(correct_board_2,player,player_row,player_col)
                            if board2 == correct_board_2:
                                return True
                            else:
                                raise Exception('This Illegal board difference')
                        else:
                            raise Exception('opposing stones should not have been removed')

                else:
                    return True
        else:
            if not diffMStones2_1:
                return True
            else:
                if not ("W" in diffMStones2_1 or "B" in diffMStones2_1):
                    raise Exception('list of difference should either be empty or have a stone in it')
                else:
                    return True


    def check_turn(self,player):
        if len(self.board_history) == 1:
            if player != "B":
                raise Exception
        elif len(self.board_history) == 2:
            if player != "W":
                raise Exception
        else:
            if self.fifth_is_empty(self.board1) and self.fifth_is_empty(self.board2):
                player_at_board1, player_at_board2 = "B", "W"
            else:
                _,_,diffMStones3_2 = self.board_difference(self.board2,self.board3)
                _,_,diffMStones2_1 = self.board_difference(self.board1,self.board2)
                player_at_board2 = self.check_turn_helper(diffMStones3_2)
                player_at_board1 = self.check_turn_helper(diffMStones2_1)
            try:
                if player == "B":
                    if player_at_board2 == "B" or player_at_board1 == "W":
                        raise Exception
                else:
                    if player_at_board2 == "W" or player_at_board1 == "B":
                        raise Exception
            except Exception:
                raise Exception('Incorrect turn')


    @staticmethod
    def check_turn_helper(diffMStones):
        if "B" in diffMStones:
            player = "B"
        elif "W" in diffMStones:
            player = "W"
        else:
            player = "pass"
        return player

    def area_counter(self, board):
        black_area, white_area = [], []
        go_board_obj = Go_Board(board)
        empty_coord_list = self.get_coord(board, " ")
        while empty_coord_list:
            current_empty_coord = empty_coord_list.pop(0)
            chain, reached, _ = go_board_obj.chain_and_reached(current_empty_coord[0], current_empty_coord[1])
            if "W" in reached and ("B" not in reached):
                for i, coord in enumerate(chain):
                    white_area.append(coord)
            elif "B" in reached and ("W" not in reached):
                for i, coord in enumerate(chain):
                    black_area.append(coord)
            empty_coord_list = [x for x in empty_coord_list if x not in chain]
        return len(white_area), len(black_area)

    @staticmethod
    def stone_counter(board):
        w, b = 0, 0
        for i, row in enumerate(board):
            for j, element in enumerate(row):
                if element == "B":
                    b += 1
                elif element == "W":
                    w += 1
        return w, b

    def check_the_score(self, board):
        w_s, b_s = self.stone_counter(board)
        w_a, b_a = self.area_counter(board)
        w, b = w_s + w_a, b_s + b_a
        return {"B": b, "W": w}

