from abc import ABC, abstractmethod
import fileinput
import re
from json import JSONDecoder, JSONDecodeError
from BackEnd import *
# import json


class FrontEnd(ABC):
    def __init__(self):
        pass

    def input_receiver(self):
        json_string = ""

        for line in fileinput.input():
            json_string += line
        return json_string

    # inspired by
    # https://stackoverflow.com/questions/27907633/multiple-json-objects-in-one-file-extract-by-python
    # decoder for stacked json obj

    def parser(self,document, pos=0, decoder=JSONDecoder()):
        NOT_WHITESPACE = re.compile(r'[^\s]')

        while True:
            match = NOT_WHITESPACE.search(document, pos)
            if not match:
                return
            pos = match.start()
            try:
                obj, pos = decoder.raw_decode(document, pos)
            except JSONDecodeError:
                raise Exception("Detected invalid input")
            yield obj

    def obj_number_checker(self,json_list):
        result =[]
        send_to_back = []
        for i,n in enumerate(json_list):
            send_to_back.append(n)
            if (i+1)%10 == 0:
                result.append(sort(send_to_back))
                send_to_back = []
        return json.dumps(result)


#### sort function check if it receives 10 obj
if __name__ == "__main__":


    frontend = FrontEnd()
    json_string = frontend.input_receiver()
    json_list = list(frontend.parser(json_string))
    result = frontend.obj_number_checker(json_list)

    print(result)




