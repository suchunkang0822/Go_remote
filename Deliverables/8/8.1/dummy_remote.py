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
        self.player_stone = stone

    def make_a_move(self,boards):
        ref = GoRuleChecker(boards)
        boards_correct = ref.sixth_resolve_history(self.player_stone)
        if boards_correct:
            rand_num = random.random()
            row, col = self.random_coord()
            if rand_num < 0.4:
                #print('passed')
                return "pass"
            elif 0.4 < rand_num:
                #print('im in',row,col)
                #print('the board is')
                #print(boards[0])
                while True:
                    if boards[0][row][col] == " ":
                        if ref.sixth_resolve_history(self.player_stone, row, col):
                            #print('im inside wow')
                            return str(col + 1) + "-" + str(row + 1)
                    row, col = self.random_coord()
            else:
                for i,row in enumerate(boards[0]):
                    for j,element in enumerate(row):
                        if element != " ":
                            row,col = i,j
                    return str(col + 1) + "-" + str(row + 1)

        else:
            return "This history makes no sense!"

    def connect(self):
        self.s.connect((self.HOST, self.PORT))

    def receive_and_send(self):
        # self.s.connect((self.HOST, self.PORT))
        json_obj = json.loads(self.s.recv(6000).decode())
        # json_obj = json.loads(self.s.recv(6000))
        #print('json received',json_obj)
        if json_obj[0] == "register":
            #print('inside register',self.register())
            self.s.send(json.dumps(self.register()).encode())
            # self.s.close()
        elif json_obj[0] == "receive-stone":
            #print('inside receive-stones')
            self.receive_stone(json_obj[1])
        elif json_obj[0] == "make-a-move":
            #print('inside make-a-move')
            #print(json_obj[1])
            self.s.send(json.dumps(self.make_a_move(json_obj[1])).encode())




if __name__ == "__main__":
    proxy = Proxy()
    proxy.connect()
    while True:
        proxy.receive_and_send()