'''
Author: Jordi Castro
ID: 010974536
'''

import sys
from socket import *
import json

SERVER = '127.0.0.1'
PORT = 6667
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# SOCK_STREAM -> TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(ADDR)

def recvHiddenWord() -> str:
    recvMsg = clientSocket.recv(1024).decode(FORMAT)
    return recvMsg
    

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
        recvData = clientSocket.recv(1024).decode(FORMAT)
        decodedData = json.loads(recvData)
        print(f'[RECEIVED FROM SERVER]: {decodedData}\n---\n')
        print(f'WORD:\n {decodedData[0]}')
        print(f'\nNUM GUESSES: {decodedData[1]}')
        print(f'\nGUESS LIST: {decodedData[2]}')


print('[START] client is starting...')
loop()

clientSocket.close()