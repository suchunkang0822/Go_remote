from CustomExceptions import *
from Referee import *
from FrontEnd import *
from importlib.machinery import SourceFileLoader
from RemoteProxy import *
from StateProxy import *
from GoBoard import *
import socket

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.PORT, self.DEFPATH = self.fetch_config()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.conn = self.create_connection()
        # self.default_player = StateProxy(self.setup_default_player())
        # self.remote_player = StateProxy(RemoteProxy(self.conn))
        self.t_style, self.n_remote = self.fetch_tournament_details()
        self.remote_connections = []
        self.n_default = 0
        self.player_map = {}


# Setup

    @staticmethod
    def fetch_config():
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default-player"]

    def bind_socket(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Binding the Host:{} Port:{}'.format(self.HOST,str(self.PORT)))
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(self.n_remote)

    @staticmethod
    def fetch_tournament_details(self):
        if len(sys.argv) != 3:
            raise Exception("Incorrect number of arguments")

        _, style, n = sys.argv
        if style not in ["--league", "--cup"] or not n.isnumeric():
            raise Exception("Arguments are incorrect")

        return style, int(n)

    def accept_connections(self):
        for c in self.remote_connections:
            c.close()

        del self.remote_connections[:]

        for i in range(self.n_remote):
            try:
                conn, _ = self.s.accept()
                self.remote_connections.append(conn)
                print('Connection has been established')
            except:
                raise Exception("Error accepting connections")

    def total_player_count(self):
        i = 0
        temp = 2 ** i if self.n_remote > 2 else 2

        while temp < self.n_remote:
            i += 1
            temp = 2 ** i

        return temp

    def setup_default_player(self):
        player_module = SourceFileLoader("Default", self.DEFPATH).load_module()
        default_player = player_module.Default()
        return default_player

    def setup_player_map(self):
        player_total = self.total_player_count()
        self.n_default = player_total - self.n_remote

        for i, conn in enumerate(self.remote_connections):
            if not conn:
                self.n_default += 1
                self.n_remote -= 1
            else:
                remote = StateProxy(RemoteProxy(conn))
                remote_name = remote.register() + str(i)
                self.player_map[remote_name] = remote

        if self.n_default > 0:
            for i in range(self.n_default):
                default = StateProxy(self.setup_default_player())
                default_name = default.register()+str(i)
                self.player_map[default_name] = default

# Game









    # def create_connection(self):
    #     self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     self.s.bind((self.HOST, self.PORT))
    #     self.s.listen()
    #     conn, _ = self.s.accept()
    #     return conn


    def game_start(self):
        winner = self.ref.play_game(self.default_player, self.remote_player)
        if winner:
            return json.dumps(winner)



            # self.conn.send(json.dumps(a).encode())
            # self.conn.close()


    def send_and_receive(self,json_data):
        try:
            if len(json_data) == 1 and json_data[0] == "register":
                name = self.remote_player.register()
                return name
            elif len(json_data) == 2 and json_data[0] == "receive-stones":
                stone = json_data[1]
                GoBoard().stone_checker(stone)
                self.remote_player.receive_stones(stone)
            elif len(json_data) == 2 and json_data[0] == "make-a-move":
                history = json_data[1]
                for i,board in enumerate(history):
                    GoBoard().board_checker(board)
                move = self.remote_player.make_a_move(history)
                return move
            else:
                return "GO has gone crazy!"
        except (ValueError,TypeError):
            return "GO has gone crazy!"

    def driver(self):
        output_list = []
        input = FrontEnd().getJson()
        for i,json_data in enumerate(input):
            output = self.send_and_receive(json_data)
            if output and output != "GO has gone crazy!":
                output_list.append(output)
            elif output == "GO has gone crazy!":
                output_list.append(output)
                self.conn.close()
                return json.dumps(output_list)
        self.conn.close()
        return json.dumps(output_list)



if __name__ == "__main__":
    admin = Admin()
    # print(admin.game_start())
    print(admin.game_start())







