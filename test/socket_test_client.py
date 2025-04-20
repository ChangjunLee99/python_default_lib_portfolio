import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from lib.util import *
import socket

util = Util()
util.parsesys()
if util.findChild("PORT") != None:
    port = int(util.getValueStr("PORT"))
else:
    port = 5001


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', port)

# 서버 소켓에 접속
client_socket.connect(server_address)

while True:
    try:
        data = input('')
        if data == 'quit':
            break
        data = data.encode()
        client_socket.send(data)
        message = client_socket.recv(1024)
        message = message.decode()
        print(f"Received: {message}")
    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
print("socket closed")