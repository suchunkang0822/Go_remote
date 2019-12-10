from FrontEnd import *
from GoRuleChecker import *
import json
import random
import socket


class Proxy(GoRuleChecker):
    Board_size = 9

    def __init__(self):
        super().__init__()
        self.player_stone = ""
        self.HOST = '127.0.0.1'
        self.PORT = 8888
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def random_coord(self):
        row = random.randrange(1,self.Board_size)
        col = random.randrange(1,self.Board_size)
        print(row,col)
        return row,col

    @staticmethod
    def register():
        # if string == "register":
        return "remote"

    def receive_stone(self,stone):
        print("stone:",stone)
        self.player_stone = stone

    def make_move(self,boards):
        ref = GoRuleChecker(boards)
        boards_correct = ref.sixth_resolve_history(self.player_stone)
        if boards_correct:
            if random.random() < 0.4:
                return "pass"
            else:
                row, col = self.random_coord()
                while boards[0][row][col] != " ":
                    if ref.sixth_resolve_history(self.player_stone, row, col):
                        return str(col + 1) + "-" + str(row + 1)
                    else:
                        row, col = self.random_coord()
                        continue
        else:
            return "This history makes no sense!"

    def receive_and_send(self):
        
        json_obj = json.loads(self.s.recv(6000).decode())
        print("WHAT? ",json_obj)
        if json_obj[0] == "register":
            self.s.send(json.dumps(self.register()).encode())
        elif json_obj[0] == "receive-stones":
            print(json_obj[0][1])
            self.receive_stone(json_obj[0][1])
        elif json_obj[0][1] == "make-a-move":
            self.s.send(self.make_move(json_obj[0][1]).encode())




if __name__ == "__main__":
    module = Proxy()
    module.s.connect((module.HOST, module.PORT))
    while True:
        module.receive_and_send()