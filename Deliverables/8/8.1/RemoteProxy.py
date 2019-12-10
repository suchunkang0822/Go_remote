from FrontEnd import FrontEnd
import json


class RemoteProxy:
    def __init__(self, conn):
        self.HOST, self.PORT, _ = self.fetch_config()
        self.player_stone = None
        self.name = None
        self.conn = conn

    def register(self):
        self.conn.send(json.dumps(["register"]).encode())
        name = json.loads(self.conn.recv(6000).decode())
        self.name = name
        return name

    def receive_stones(self, stone):
        self.player_stone = stone
        self.conn.send(json.dumps(["receive-stones", stone]).encode())

    def make_a_move(self, boards):
        # print('why am i not in')
        # print('this is make a move history',boards)
        self.conn.send(json.dumps(["make-a-move", boards]).encode())
        move = json.loads(self.conn.recv(6000).decode())
        return move

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]
