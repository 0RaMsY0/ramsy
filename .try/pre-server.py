import socket
from vidstream import StreamingServer
import threading
host = socket.gethostbyname(socket.gethostname())
port = 1827

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host , port))

server.listen(3)
add, ip = server.accept()
print(f"Connected {ip}")
while True:
    dd = input("\r>>")
    if dd:
        if dd == "start stream":
            add.send(dd.encode())
            ff = StreamingServer(host, 8989)
            ggff = threading.Thread(
                target=ff.start_server()
            )
            ggff.start()
        if dd == "stop stream":
            add.send(dd.encode())