'''
Author: Jordi Castro
ID: 010974536
'''

import sys
from socket import *

SERVER = '127.0.0.1'
PORT = 6667
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# SOCK_STREAM -> TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(ADDR)


# .send -> encode
msg = '[CLIENT]testing send'.encode(FORMAT)

clientSocket.send(msg)

# .recv(1024) -> decode

recv_msg = clientSocket.recv(1024).decode(FORMAT)

print(f'[RECEIVED FROM SERVER]: {recv_msg}')

clientSocket.close()