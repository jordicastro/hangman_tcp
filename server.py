'''
Author: Jordi Castro
ID: 010974536
'''

import sys
import random
from socket import *
import json

SERVER = '127.0.0.1'
PORT = 6667
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
guessList = []
numGuesses = 0
NUM_LOSS = 7
WIN = False
LOSS = False

WORDS = ['apple', 'galaxy', 'puzzle', 'axiom', 'notebook', 'pajama', 'octupus', 'subway', 'oxygen', 'copyright']

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(ADDR)
serverSocket.listen(1)

print('server ready to receive.')

def handleClient(word):
    global WIN, LOSS
    guess = ''
    # establishing connection with client
    connSocket, addr = serverSocket.accept()
    # initial send
    connSocket.send(hideWord(word, guess).encode(FORMAT))
    while not (WIN or LOSS):
        # display hiddenword to client
        guess = connSocket.recv(1024).decode(FORMAT)
        hiddenWord = handleGuess(word, guess)
        # send the hidden word, num guesses, and the guess list in json -> dumps string data
        data = [hiddenWord, numGuesses, guessList]
        encodedData = json.dumps(data).encode(FORMAT)
        connSocket.send(encodedData)

    if WIN:
        msg = f'you won! the word was {word}'
        connSocket.send(msg.encode(FORMAT))
        exit
    if LOSS:
        msg = f'you lost! the word was {word}'
        connSocket.send(msg.encode(FORMAT))
        exit
    connSocket.close()
    # handleWin() | handleLoss()
def handleGuess(word, guess):
    global guessList, numGuesses, LOSS
    # exceeds num guesses:
    if numGuesses == NUM_LOSS:
        print('exceeded num guesses! client lost.')
        LOSS = True
    # duplicate guess
    elif guess in guessList:
        print(f'already used this guess. {guess}\nhandling duplicate guess...')
        handleDuplicateGuess()
    # correct guess, update hiddenWord, guessList, & numGuesses
    elif guess in word:
        print(f'guess {guess} found in word!\n hiding word')
        guessList.append(guess)
        numGuesses += 1
        print(f'appended list: {guessList}\nnum guesses = {numGuesses}')
    # incorrect guess
    else:
        print(f'wrong guess {guess}\nupdating guess list and guesses')
        guessList.append(guess)
        numGuesses+=1
        print(f'appended list: {guessList}\nnum guesses = {numGuesses}')

    return hideWord(word, guess)
    
        

def handleDuplicateGuess():
    pass

def hideWord(word, guess) -> str:
    global WIN
    hiddenWord = ''
    for char in word:
        if char in guessList:
            hiddenWord += char + ' '
        else:
            hiddenWord += '_ '
    print(f'hidden word is {hiddenWord}')
    if '_' not in hiddenWord:
        WIN = True
        print(f'WIN is {WIN}')
    return hiddenWord

def start():
    choice = input('enter a word or enter 0 for a randomized word: ')
    if choice == '0':
        word = random.choice(WORDS)
    else:
        word = choice.split()[0].lower()

    print(f'the word is {word}\nhandling client...\n')

    handleClient(word)




print('[START] server is starting...')
start()