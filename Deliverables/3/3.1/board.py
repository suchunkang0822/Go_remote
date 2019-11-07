import abc
from FrontEnd import *
from BackEnd import*


class Interface(abc.ABC):
    def __init__(self):
        pass

    @abstractmethod
    def is_occupied(self,point):
        pass
    @abstractmethod
    def occupies(self,point,stone):
        pass
    @abstractmethod
    def is_reachable(self,point,maybestone):
        pass
    @abstractmethod
    def place(self,point,stone):
        pass
    @abstractmethod
    def remove(self,stone,point):
        pass
    @abstractmethod
    def get_points(self,maybestone):
        pass


class Board(Interface):


    def __init__(self,board):
        super().__init__()
        self.maybe_stone = ["B", "W", " "]
        self.board = self.board_checker_set(board)
        self.visited = [[0]*19 for _ in range(19)]
        self.neighbors = [self.get_valid_neighbors([i,j]) for i in range(19) for j in range(19)]




    def point_parser(self,point):
        coordinate = re.findall(r'\d+',point)
        coordinate = list(map(lambda x: int(x)-1,coordinate))
        coordinate[0], coordinate[1] = coordinate[1], coordinate[0]
        if len(coordinate) != 2 or not isinstance(point,str):
            raise TypeError("There should only be two numbers in the format of \"int-int\"")
        else:
            return coordinate

    def stone_checker(self,stone):
        # print("this is stone")
        # print(stone)
        if stone not in ("B", "W"):
            raise TypeError("stone must be either \"B\" or \"W\"")

    def maybe_stone_checker(self,maybe_stone):
        if maybe_stone not in ("B", "W"," "):
            raise TypeError("element other than maybe_stone detected")

    def board_checker_set(self,board):
        if not(len(board) == 19 and len(board[0]) == 19):
            raise TypeError("board must be list of 19 by 19 ")
        for i,row in enumerate(board):
            for j,element in enumerate(row):
                # if element not in self.maybe_stone:
                self.maybe_stone_checker(element)
        return board

    def is_occupied(self,point):
        coordinate = self.point_parser(point)
        if self.board[coordinate[0]][coordinate[1]] in ("B", "W"):
            return True
        else:
            return False

    def occupies(self,stone,point):
        self.stone_checker(stone)
        coordinate = self.point_parser(point)
        if self.board[coordinate[0]][coordinate[1]] == stone:
            return True
        else:
            return False

    def is_on_board(self,coordinate):
        return 0 <= coordinate[0] <= 18 and 0 <= coordinate[1] <= 18

    def get_valid_neighbors(self,coordinate):
        possible_neighbors = [[coordinate[0],coordinate[1] - 1],
                              [coordinate[0]-1, coordinate[1]],
                              [coordinate[0], coordinate[1] + 1],
                              [coordinate[0] + 1, coordinate[1]]]
        return [n for n in possible_neighbors if self.is_on_board(n)]


    def is_reachable(self,point,maybe_stone):
        coordinate = self.point_parser(point)
        self.maybe_stone_checker(maybe_stone)
        coordinate_stone = self.board[coordinate[0]][coordinate[1]]
        if coordinate_stone == maybe_stone:
            return True
        else:
            chain = [coordinate]
            reached = []
            frontier = [coordinate]
            while frontier:
                current = frontier.pop()
                chain.append(current)
                for n in self.neighbors[current[0]*19+current[1]]:
                    if self.board[n[0]][n[1]] == coordinate_stone and n not in chain:
                        frontier.append(n)
                    elif self.board[n[0]][n[1]] != coordinate_stone:
                        reached.append(self.board[n[0]][n[1]])
            if maybe_stone in reached:
                return True
            else:
                return False

    def place(self,stone,point):
        self.stone_checker(stone)
        coordinate = self.point_parser(point)
        if self.board[coordinate[0]][coordinate[1]] == " ":
            self.board[coordinate[0]][coordinate[1]] = stone
            return self.board
        else:
            return 'This seat is taken!'

    def remove(self,stone,point):
        self.stone_checker(stone)
        coordinate = self.point_parser(point)
        if self.board[coordinate[0]][coordinate[1]] == stone:
            self.board[coordinate[0]][coordinate[1]] = " "
            return self.board
        else:
            return "I am just a board! I cannot remove what is not there!"

    def coordinate_to_point(self,coordinate):
        return str(coordinate[1]+1)+"-"+str(coordinate[0]+1)


    def get_points(self,maybe_stone):
        result_list = []
        for i,n in enumerate(self.board):
            for j,k in enumerate(n):
                if k == maybe_stone:
                    result_list.append(self.coordinate_to_point([i,j]))
        return sort(result_list)

class BoardFrontEnd:
    def __init__(self):
        self.query = ("occupied?","occupies?","reachable?")
        self.command = ("place", "remove", "get-points")
    def question(self,list_of_list):
        result = []
        for index,el_list in enumerate(list_of_list):
            board = el_list[0]
            command_or_query = el_list[1]
            # if command_or_query[0] not in self.query and command_or_query not in self.command:
            if command_or_query[0] not in ("occupied?","occupies?","reachable?","place","remove", "get-points"):
                raise TypeError("Please type valid query or command")
            go_board = Board(board)

            if command_or_query[0] == "occupied?":
                result.append(go_board.is_occupied(command_or_query[1]))
            elif command_or_query[0] == "occupies?":
                result.append(go_board.occupies(command_or_query[1],command_or_query[2]))
            elif command_or_query[0] == "reachable?":
                result.append(go_board.is_reachable(command_or_query[1],command_or_query[2]))
            elif command_or_query[0] == "place":
                result.append(go_board.place(command_or_query[1],command_or_query[2]))
            elif command_or_query[0] == "remove":
                result.append(go_board.remove(command_or_query[1],command_or_query[2]))
            elif command_or_query[0] == "get-points":
                result.append(go_board.get_points(command_or_query[1]))
        return json.dumps(result)

# , indent=4



if __name__ == '__main__':
    f = FrontEnd()
    json_string = f.input_receiver()
    json_list = list(f.parser(json_string))

    go_board = BoardFrontEnd()

    print(go_board.question(json_list))












