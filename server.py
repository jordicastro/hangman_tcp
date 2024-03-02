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

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(ADDR)
serverSocket.listen(1)

print('server ready to receive.')

while 1:
    connSocket, addr = serverSocket.accept()
    sentence = connSocket.recv(1024).decode(FORMAT)
    sentence = sentence + ' [SERVER]: added this part, sending back your way!'.encode(FORMAT)

    connSocket.send(sentence)

    connSocket.close()

