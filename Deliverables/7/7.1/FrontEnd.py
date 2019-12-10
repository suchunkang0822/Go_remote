from abc import ABC, abstractmethod
import fileinput
import re
from json import JSONDecoder, JSONDecodeError
from BackEnd import *
import sys


class FrontEnd(ABC):
    def __init__(self):
        pass

    def getJson(self):
        jsonInputs = []
        currentObj = ""
        for line in sys.stdin:
            currentObj += line
            currentObj = currentObj.lstrip()
            try:
                currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
                jsonInputs.append(currentDecodedMessage[0])
                while currentDecodedMessage[1] < len(currentObj):
                    currentObj = currentObj[currentDecodedMessage[1] + 1:]
                    try:
                        currentDecodedMessage = json.JSONDecoder().raw_decode(currentObj)
                        jsonInputs.append(currentDecodedMessage[0])
                    except ValueError:
                        pass
                currentObj = ""
            except ValueError:
                pass

        return jsonInputs



    def input_receiver(self,file_name=None):
        json_string = ""
        if file_name:
            for line in fileinput.input(files=file_name):
                json_string += line
        else:
            for line in fileinput.input():
                json_string += line
        return json_string


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


def abstract_front_end():
    f = FrontEnd()
    json_string = f.input_receiver()
    list_json = list(f.parser(json_string))
    return list_json

# sort function check if it receives 10 obj


if __name__ == "__main__":

    frontend = FrontEnd()
    json_list = abstract_front_end()
    result = frontend.obj_number_checker(json_list)

    print(result)




