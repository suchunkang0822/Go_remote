from FrontEnd import FrontEnd
from Remote import Remote
import socket


class PlayerProxy:
    def __init__(self, Player):
        self.registered = None
        self.received = None
        self.player = Player
        # self.player = Remote() TODO: should we use ths implementation

    def receive_data(self):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.player.Host,self.player.Port))
            s.listen()
            request =b""
            conn,addr = s.accept()
            with conn:
                # print('Connected by',addr)
                # while True:
                data = conn.recv(6000)
                    # request += data
                    # if len(data) < 1024:
                    #     break

            decoded_data = request.decode('utf-8')
            json_command = list(FrontEnd().parser(decoded_data))
            # result = self.driver(json_list)
            # conn.sendall(result.encode())
            s.close()
            if !self.verify_command(json_command):
                return False
            
            return json_command
                
    
    def verify_command(self, command):
        if command == "register":
            self.registered = True 
            return True
        elif command == "receive-stones":
            if self.registered == True:
                self.received = True
                return True
        else:
            if self.registered == True and self.received == True:
               return True

        return False

