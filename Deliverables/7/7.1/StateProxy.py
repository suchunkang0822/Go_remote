
class StateProxy:
    def __init__(self, player):
        self.player = player
        self.registered = False
        self.received = False

    def register(self):
        if not self.registered and not self.received:
            self.registered = True
            return self.player.register()
        else:
            raise ValueError

    def receive_stone(self,stone):
        if self.registered and not self.received:
            self.received = True
            return self.player.receive_stone(stone)
        else:
            raise ValueError

    def make_a_move(self, boards):
        if self.registered and self.received:
            return self.player.make_a_move(boards)
        raise ValueError






    # def receive_all(self):
    #     response = b""
    #     while True:
    #         res = self.player.conn.recv(1024)
    #         if not res:
    #             break
    #         response += res
    #     return response
    #
    # def receive(self):
    #     input = self.receive_all()
    #     list_json_data = list(FrontEnd().parser(input))
    #     for i,json_data in enumerate(list_json_data):
    #         self.player.send(json_data)
    #
    # def send(self,json_data):
    #     try:
    #         if len(json_data) == 1 and json_data[0] == "register":
    #             self.register()
    #             # name = self.player.register()
    #             #print(json.dumps(name).encode())
    #         elif len(json_data) == 2 and json_data[0] == "receive-stones":
    #             stone = json_data[1]
    #             self.receive_stone()
    #             # self.player.receive_stone(stone)
    #         elif len(json_data) == 2 and json_data[0]== "make-move":
    #             history = json_data[1]
    #             self.make_a_move()
    #             # move = self.player.make_move(history)
    #             #print(json.dumps(move).encode())
    #         else:
    #             return "GO has gone crazy!"
    #     except ValueError:
    #         return "GO has gone crazy!"









# if __name__ == "__main__":
#     pass