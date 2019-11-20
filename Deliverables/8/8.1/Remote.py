from FrontEnd import *
import socket
import json

class Remote:
    def __init__(self,host,port):
        self.Host, self.Port, _ = self.fetch_config()

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default"]

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.Host, self.Port))
            s.sendall(FrontEnd().input_receiver().encode())
            # data = self.receive_all(s)
            data = s.recv(6000)
            return data.decode()



if __name__ == "__main__":