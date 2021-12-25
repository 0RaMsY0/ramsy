"""
    this code created by 0RaMsY0
"""
import argparse
import time, os, sys
from typing import Text
from server.name import SERVER_TYPES
from assets.colors import colors
from assets.symbols import Sminess, Splus, Swarning, Ssowrd
from payloads.name import PAYLOADS_TYPES
from warnings.WarningHandler import InvaliedEntry
#error handler you will find the script in warnings\WarningHandler.py directory
CR = colors

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-s", "--show", help="take an argument [servers, payloads]")
PARSER.add_argument("-u", "--use" , help="command to start a server [take an argument]")
PARSER.add_argument( "-S", "--set", help="command for creating a payload [take an argument]")
PARSER.add_argument("-t", "--target", help="commmand to see targets info [take an argument]")
ARGS = PARSER.parse_args()
__SHOW__ = ARGS.show
__USE__ = ARGS.use
__SET__ = ARGS.set
__TARGET__ = ARGS.target

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