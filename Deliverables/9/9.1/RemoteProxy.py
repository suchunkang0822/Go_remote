from FrontEnd import FrontEnd
import socket
import json


class RemoteProxy():
    def __init__(self, conn):
        self.HOST, self.PORT, _ = self.fetch_config()
        self.player_stone = None
        self.name = None
        self.conn = conn
        

    def register(self):
        json_data = json.dumps(["register"]).encode()
        self.conn.send(json_data)
        
        data = self.conn.recv(6000).decode()
        name = json.loads(data)
        self.name = name
        return name
    
    def receive_stones(self, stone):
        print('inside receive stoen',stone)
        self.player_stone = stone
        self.conn.send(json.dumps(["receive-stones", stone]).encode())
    
    def make_move(self, boards):
        json_data = json.dumps(["make-a-move", boards]).encode()
        self.conn.send(json_data)
        print('send move ',json_data)
        move = json.loads(self.conn.recv(6000).decode())
        print('hrllo')
        return move

    def end_game(self):
        self.conn.send(json.dumps(["end-game"]).encode())
        response = json.loads(self.conn.recv(6000).decode())
        return response

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    
    # def connect(self,data):
    #     self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.s.connect((self.HOST, self.HOST))  
            # s.sendall(json.dumps(data).encode())
            # data = s.recv(6000)
            # return data.decode()
    
    # def receive_and_send(self):
    #     data = self.s.recv(6000)
    #     json_data = json.loads(data.decode('utf-8'))
    #     if len(json_data) == 1 and json_data[0] == "register":
    #         name = self.player.register()
    #         self.s.sendall(json.dumps(name).encode())
    #     elif len(json_data) == 2 and json_data[0] == "receive-stones":
    #         stone = json_data[1]
    #         self.player.receive_stones(stone)
    #     elif len(json_data) == 2 and json_data[0]== "make-move":
    #         history = json_data[1]
    #         move = self.player.make_move(history)
    #         self.s.sendall(json.dumps(move).encode())
    #     else:
    #         return "GO has gone crazy!"

    
        





# if __name__ == '__main__':
#     remote_player = Remote(Player())
#     # remote_player.verify_protocol(remote_player._wrapped.register())
#     remote_player.connect()
#     while True:
#         remote_player.receive_and_send()

#     PlayerProxy(Remote()).connect()