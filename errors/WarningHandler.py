from assets.symbols  import *
from assets.colors import *
import sys
def InvaliedEntry(element):
    if element == "show":
        print(f" {Sminess}{CR.red()} Invalied argument try {CR.yellow()} [{CR.blue()}servers, payloads{CR.yellow()}] {CR.white()}")

def NoLhostSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-sh {CR.blue()}[--SocketLhost] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()

def NoLportSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-sp {CR.blue()}[--SocketLport] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()

def NoCameraStreamingPortSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-csp {CR.blue()}[--CameraStreamingPort] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()

def NoAudioStreamingPortSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-asp {CR.blue()}[--AudioStreamingPort] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()

def NoScreenStreamingPortSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-ssp {CR.blue()}[--ScreenStreamingPort] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()

def NoReverShellPort():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-rsp {CR.blue()}[--ReverseShellPort] {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")
    sys.exit()