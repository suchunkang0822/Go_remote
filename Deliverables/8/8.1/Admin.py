from Referee import Referee
import socket
import importlib.util

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.POST, self.DEFPATH = self.fetch_config()
        spec = importlib.util.spec_from_file_location("Default", "self.DEFPATH")



    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default"]

    def receive_data(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST,PORT))
            s.listen()
            request =b""
            conn,addr = s.accept()
            with conn:
                # print('Connected by',addr)
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024:
                        break

                decoded_data = request.decode('utf-8')
                json_list = list(FrontEnd().parser(decoded_data))
                result = self.driver(json_list)
                conn.sendall(result.encode())
                s.close()



# starts server and accepts connection from remote
# creates proxy????
# loads local player from config
#
