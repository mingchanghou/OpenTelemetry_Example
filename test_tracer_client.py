import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("", 10500))
sock.send(b"isAlive")
response = b''
while True:
    recv = sock.recv(4096)
    response += recv
    if len(recv) < 4096:
        break
sock.close()
print(response)
