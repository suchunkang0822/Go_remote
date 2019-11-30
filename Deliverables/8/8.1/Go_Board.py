import abc
from FrontEnd import *
from BackEnd import *


class Interface(abc.ABC):
    def __init__(self):
        pass

    # @abstractmethod
    # def is_occupied(self,point):
    #     pass
    # @abstractmethod
    # def occupies(self,point,stone):
    #     pass
    # @abstractmethod
    # def is_reachable(self,point,maybestone):
    #     pass
    # @abstractmethod
    # def place(self,point,stone):
    #     pass
    # @abstractmethod
    # def remove(self,stone,point):
    #     pass
    # @abstractmethod
    # def get_points(self,maybestone):
    #     pass


class Go_Board(Interface):
    Board_Size = 9
    Maybe_Stone = ["B", "W", " "]
    Stone = ["B", "W"]

    def __init__(self,board=[]):
        super().__init__()
        if board:
            self.board = self.board_checker(board)
        else:
            self.board = [[" " for i in range(self.Board_Size)] for j in range(self.Board_Size)]
        self.neighbors = [self.get_valid_neighbors([i,j]) for i in range(self.Board_Size) for j in range(self.Board_Size)]

    def point_parser(self,point):
        coordinate = re.findall(r'\d+',point)
        coordinate = list(map(lambda x: int(x)-1,coordinate))
        # coordinate[0], coordinate[1] = coordinate[1], coordinate[0]
        if len(coordinate) != 2 or not isinstance(point,str):
            raise TypeError("There should only be two numbers in the format of int-int")
        else:
            return coordinate[1], coordinate[0]

    def stone_checker(self,stone):
        if stone not in self.Stone:
            raise TypeError("stone must be either B or W")

    def maybe_stone_checker(self,maybe_stone):
        if maybe_stone not in self.Maybe_Stone:
            raise TypeError("element other than maybe_stone detected")

    def board_checker(self,board):
        #print('what is len(board)',len(board),len(board[0]))
        #print(board)
        if not(len(board) == self.Board_Size and len(board[0]) == self.Board_Size):
            raise TypeError("board must be list of {} by {} ".format(self.Board_Size,self.Board_Size))
        for i,row in enumerate(board):
            for j,element in enumerate(row):
                self.maybe_stone_checker(element)
        return board

    def is_occupied(self,row,col):
        if self.board[row][col] in self.Stone:
            return True
        else:
            return False

    def occupies(self,stone,row,col):
        self.stone_checker(stone)
        if self.board[row][col] == stone:
            return True
        else:
            return False

    def is_on_board(self, coordinate):
        return 0 <= coordinate[0] <= self.Board_Size -1 and 0 <= coordinate[1] <= self.Board_Size -1

    def get_valid_neighbors(self,coordinate):
        possible_neighbors = [[coordinate[0],coordinate[1] - 1],
                              [coordinate[0]-1, coordinate[1]],
                              [coordinate[0], coordinate[1] + 1],
                              [coordinate[0] + 1, coordinate[1]]]
        return [n for n in possible_neighbors if self.is_on_board(n)]

    def chain_and_reached(self,row,col):
        coordinate_stone = self.board[row][col]
        visited, chain, reached, reached_coord = [], [], [], []
        frontier = [[row, col]]
        while frontier:
            current = frontier.pop()
            if current not in chain:
                chain.append(current)
            for n in self.neighbors[current[0] * self.Board_Size + current[1]]:
                if self.board[n[0]][n[1]] == coordinate_stone:
                    if n not in chain:
                        frontier.append(n)
                elif self.board[n[0]][n[1]] != coordinate_stone:
                    if n not in visited:
                        reached.append(self.board[n[0]][n[1]])
                        reached_coord.append(n)
                visited.append(n)

        return chain, reached, reached_coord

    def is_reachable(self,maybe_stone,row,col):
        coordinate_stone = self.board[row][col]
        if coordinate_stone == maybe_stone:
            return True
        else:
            _, reached, _ = self.chain_and_reached(row,col)
            if maybe_stone in reached:
                return True
            else:
                return False

    def place(self,stone,row,col):
        self.stone_checker(stone)
        if self.board[row][col] == " ":
            copy = [row.copy() for row in self.board]
            copy[row][col] = stone
            return copy
        else:
            return 'This seat is taken!'

    def remove(self,stone,row,col,in_place = None):
        self.stone_checker(stone)
        if in_place:
            self.board[row][col] = " "
        else:
            if self.board[row][col] == stone:
                copy = [row.copy() for row in self.board]
                copy[row][col] = " "
                return copy
            else:
                return "I am just a board! I cannot remove what is not there!"


    @staticmethod
    def coordinate_to_point(self,coordinate):
        return str(coordinate[1]+1)+"-"+str(coordinate[0]+1)

    @staticmethod
    def get_points(self,maybe_stone):
        result_list = []
        for i,n in enumerate(self.board):
            for j,k in enumerate(n):
                if k == maybe_stone:
                    result_list.append(self.coordinate_to_point([i,j]))
        return sort(result_list)

    @staticmethod
    def coord_checker(row, col):
        if 0 > row or row > 18 or 0 > col or col > 18:
            raise TypeError("row and col must be greater than 0 and less than 19")

    @staticmethod
    def get_coord(board,maybe_stone):
        result_list = []
        for i,n in enumerate(board):
            for j,k in enumerate(n):
                if k == maybe_stone:
                    result_list.append([i,j])
        return result_list


class BoardFrontEnd:
    Query = ("occupied?","occupies?","reachable?")
    Command = ("place", "remove", "get-points")

    def __init__(self):
        pass

    def extract_coordinate(self,board,command_or_query):
        board_obj = Go_Board(board)
        if command_or_query[0] in ("occupied?","reachable?"):
            return board_obj.point_parser(command_or_query[1])
        elif command_or_query[0] in ("place","remove", "occupies?"):
            return board_obj.point_parser(command_or_query[2])
        else:
            return None,None

    def answer_command_query(self, board, command_or_query, row, col):
        board_obj = Go_Board(board)
        if command_or_query[0] == "occupied?":
            return board_obj.is_occupied(row, col)
        elif command_or_query[0] == "occupies?":
            return board_obj.occupies(command_or_query[1], row, col)
        elif command_or_query[0] == "reachable?":
            return board_obj.is_reachable(command_or_query[2], row, col)
        elif command_or_query[0] == "place":
            return board_obj.place(command_or_query[1], row, col)
        elif command_or_query[0] == "remove":
            return board_obj.remove(command_or_query[1], row, col)
        elif command_or_query[0] == "get-points":
            return board_obj.get_points(command_or_query[1])

    def question(self,list_of_list):
        result = []
        for index,el_list in enumerate(list_of_list):
            board = el_list[0]
            command_or_query = el_list[1]
            if command_or_query[0] not in ("occupied?","occupies?","reachable?","place","remove", "get-points"):
                raise TypeError("Please type valid query or command")
            row, col = self.extract_coordinate(board, command_or_query)
            result.append(self.answer_command_query(board,command_or_query,row,col))
        return json.dumps(result)


if __name__ == '__main__':
    f = FrontEnd()
    json_string = f.input_receiver()
    json_list = list(f.parser(json_string))

    go_board = Go_Board()

    #print(go_board.question(json_list))












