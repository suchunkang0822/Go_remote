from Referee import Referee
import socket
import json
from FrontEnd import FrontEnd
import importlib.util
from PlayerProxy import PlayerProxy
from Remote import Remote

class Admin:
    def __init__(self):
        self.ref = Referee()
        self.HOST, self.POST, self.DEFPATH = self.fetch_config()
        # spec = importlib.util.spec_from_file_location("Default", "self.DEFPATH")
        # temp = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(temp)
        # foo.MyClass()

    def fetch_config(self):
        json_string = FrontEnd().input_receiver('go.config')
        python_obj = json.loads(json_string)
        return python_obj["IP"], python_obj["port"], python_obj["default"]

    def setup_players(self):
        remote = Remote()
        remoteProxy = PlayerProxy(remote)
        
        



# starts server and accepts connection from remote
# creates proxy????
# loads local player from config
#
