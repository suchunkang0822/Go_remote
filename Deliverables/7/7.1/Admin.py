from Referee import *
from FrontEnd import *
from importlib.machinery import SourceFileLoader
from RemoteProxy import *
from StateProxy import *
import socket

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.s = None
        self.conn = self.create_connection()
        # self.default_player = StateProxy(self.setup_default_player())
        self.remote_player = StateProxy(RemoteProxy(self.conn))


    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()
        conn, _ = self.s.accept()
        return conn
            # with conn:
            #     while True:
            #         data = conn.recv(6000)
            #         if len(data) < 6000:
            #             break
            # data = conn.recv(6000)
            # decoded_data = data.decode('utf-8')
            # json_list = list(FrontEnd().parser(decoded_data))
            # return json_list
        

    # def game_start(self):

    #     winner = self.ref.play_game(self.default_player, self.remote_player)
    #     if winner:
    #         return json.dumps(winner)


            # self.conn.send(json.dumps(a).encode())
            # self.conn.close()

    def setup_default_player(self):
        player_module = SourceFileLoader("Default", self.DEFPATH).load_module()
        default_player = player_module.Default()
        return default_player

    def send_and_receive(self,json_data):
        try:
            if len(json_data) == 1 and json_data[0] == "register":
                name = self.remote_player.register()
                return name
                # print(json.dumps(name).encode())
            elif len(json_data) == 2 and json_data[0] == "receive-stones":
                stone = json_data[1]
                self.remote_player.receive_stone(stone)
            elif len(json_data) == 2 and json_data[0]== "make-a-move":
                history = json_data[1]
                move = self.remote_player.make_a_move(history)
                return move
                # print(json.dumps(move).encode())
            else:
                return "GO has gone crazy!"
        except ValueError:
            return "GO has gone crazy!"

    def driver(self):
        output_list = []
        input = FrontEnd().input_receiver()
        list_json_data = list(FrontEnd().parser(input))
        for i,json_data in enumerate(list_json_data):
            output = self.send_and_receive(json_data)
            if output and output != "GO has gone crazy!":
                output_list.append(output)
            elif output == "GO has gone crazy!":
                output_list.append(output)
                return json.dumps(output_list)
        return json.dumps(output_list)



if __name__ == "__main__":
    admin = Admin()
    # print(admin.game_start())
    print(admin.driver())






