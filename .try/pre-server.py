import socket

host = socket.gethostbyname(socket.gethostname())
port = 1827

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host , port))

server.listen(3)

while True:
    server.listen(3)
    add, ip = server.accept()
    print(f"Connected {ip}")
    x = add.recv(10000)
    print(x.decode())
    if KeyboardInterrupt:
        server.close()
