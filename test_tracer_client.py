import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("", 10500))
sock.send(b"isAlive")
response = sock.recv(4096)
sock.close()
print(response.decode())
