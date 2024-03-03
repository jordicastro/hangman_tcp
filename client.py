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

def recvHiddenWord() -> str:
    recv_msg = clientSocket.recv(1024).decode(FORMAT)
    return recv_msg
    

def loop():
    # initial hidden word
    print(recvHiddenWord())
    while 1:
        # recieve hiddenWord from server:

        # prompt client for guess
        guess = input('\nenter a letter to guess: ').split()[0]
        # .send -> encode
        msg = guess.encode(FORMAT)

        clientSocket.send(msg)

        # .recv(1024) -> decode
        print('waiting for server to transmit message...')
        recv_msg = clientSocket.recv(1024).decode(FORMAT)

        print(f'[RECEIVED FROM SERVER]: {recv_msg}')


print('[START] client is starting...')
loop()

clientSocket.close()