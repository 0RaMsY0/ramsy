from assets.symbols  import *
from assets.colors import *

def InvaliedEntry(element):
    if element == "show":
        print(f"        {Sminess}{CR.red()} Invalied argument try {CR.yellow()} [{CR.blue()}servers, payloads{CR.yellow()}] {CR.white()}")

def NoLhostSpec():
    print(f" {Sminess}{CR.red()} The {CR.yellow()}-sh {CR.red()}parameters is required and we didn't find any value for it in the {CR.yellow()}config.json{CR.white()}")