from FrontEnd import *
from GoRuleChecker import *
import json
import random
import socket
import time


class Proxy(GoRuleChecker):
    Board_size = 9

    def __init__(self):
        super().__init__()
        self.player_stone = ""
        self.HOST = 'localhost'
        self.PORT = 8888
        self.s = None

    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((self.HOST,self.PORT))
        except:
            time.sleep(2)
            self.connect()

    def random_coord(self):
        row = random.randrange(1,self.Board_size)
        col = random.randrange(1,self.Board_size)
        
        return row,col


    @staticmethod
    def register():
        # if string == "register":
        return "remote"

    def receive_stones(self,stone):
        print("stone:",stone)
        self.player_stone = stone

    def make_move(self,boards):
        ref = GoRuleChecker(boards)
        boards_correct = ref.sixth_resolve_history(self.player_stone)
        if boards_correct:
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
            raise Exception("boards history not valid")

    def end_game(self):
        return "OK"


    def receive_and_send(self):
        name = self.s.recv(6000)
        print("name",name)
        json_obj = json.loads(name.decode())
        print("WHAT? ",json_obj)
        if json_obj[0] == "register":
            self.s.send(json.dumps(self.register()).encode())
        elif json_obj[0] == "receive-stones":
            print(json_obj)
            self.receive_stones(json_obj[1])
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
    module.connect()
    # module.s.connect((module.HOST, module.PORT))
    while True:
        if module.receive_and_send() == "OK":
            break
    module.s.close()