'''
Author: Jordi Castro
ID: 010974536
'''

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
    state = True
    gap = '\n\n-------------------------\n\n'
    # initial hidden word
    print(recvHiddenWord())
    while state:

        # prompt client for guess
        guess = input('\nenter a letter to guess: ').split()[0]
        # .send -> encode
        msg = guess.encode(FORMAT)

        clientSocket.send(msg)

        # .recv(1024) -> decode
        recvData = clientSocket.recv(1024).decode(FORMAT)
        decodedData = json.loads(recvData)
        print(f'{gap}{decodedData[0]}')
        print(f'\nREMAINING GUESSES: {7-decodedData[1]}')
        print(f'\nGUESS LIST: {decodedData[2]}\n')
        state = decodedData[3]

print('[START] client is starting...\n')
loop()

clientSocket.close()
print('[DONE] socket successfully closed.')