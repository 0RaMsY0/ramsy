from assets.symbols  import *
from assets.colors import *

def InvaliedEntry(element):
    if element == "show":
        print(f"        {Sminess}{CR.red()} Invalied argument try {CR.yellow()} [{CR.blue()}servers, payloads{CR.yellow()}] {CR.white()}")