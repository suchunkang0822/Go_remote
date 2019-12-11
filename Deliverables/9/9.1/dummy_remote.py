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
        # boards_correct = ref.sixth_resolve_history(self.player_stone)
        if True:
            print("correct boards")
            if random.random() <= 0.2:
                return "pass"
            else:
                row, col = self.random_coord()
                if boards[0][row][col] == " ":
                    print("sending",row,col)
                    return str(col + 1) + "-" + str(row + 1)
                while boards[0][row][col] != " ":
                    if ref.sixth_resolve_history(self.player_stone, row, col) or True :
                        print("sending",row,col)
                        return str(col + 1) + "-" + str(row + 1)
                    else:
                        row, col = self.random_coord()
                        continue
                print("bleh bleh blej")
        else:
            return "This history makes no sense!"

    def end_game(self):
        return "OK"


    def receive_and_send(self):
        name = self.s.recv(6000)
        print("name",name)
        json_obj = json.loads(name.decode())
        print("WHAT? ",json_obj)
        if json_obj[0] == "register":
            self.s.send(json.dumps(self.register()).encode())
        elif json_obj[0] == "receive-stone":
            print(json_obj)
            self.receive_stone(json_obj[1])
        elif json_obj[0] == "make-a-move":
            temp = self.make_move(json_obj[1])
            print("temp",temp)
            self.s.send(json.dumps(temp).encode())
        elif json_obj[0] == "end-game":
            response = self.end_game()
            self.s.send(json.dumps(response).encode())
            return response
        else:
            raise Exception("Incorrect command")




if __name__ == "__main__":
    module = Proxy()
    module.s.connect((module.HOST, module.PORT))
    while True:
        if module.receive_and_send() == "OK":
            break