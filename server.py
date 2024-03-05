'''
Author: Jordi Castro
Date: 3/5/24
'''

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
STATE = True

WORDS = ['apple', 'galaxy', 'puzzle', 'axiom', 'notebook', 'pajama', 'octupus', 'subway', 'oxygen', 'copyright']

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

serverSocket.bind(ADDR)
serverSocket.listen(1)

print('server ready to receive.')

def handleClient(word):
    global WIN, LOSS, STATE
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
        if STATE:
            data = [hiddenWord, numGuesses, guessList, STATE]
            encodedData = json.dumps(data).encode(FORMAT)
            connSocket.send(encodedData)

    if WIN:
        msg = f'you won! the word was {word}'
    if LOSS:
        msg = f'you lost! the word was {word}'
    # guessList.append(guess)
    finalData = [msg, numGuesses, guessList, STATE]
    encodedFinalData = json.dumps(finalData).encode(FORMAT)
    connSocket.send(encodedFinalData)
    connSocket.close()
    
def handleGuess(word, guess):
    global guessList, numGuesses, LOSS, STATE
    # exceeds num guesses:
    if numGuesses == NUM_LOSS:
        print('exceeded num guesses! client lost.')
        LOSS = True
        STATE = False
        exit
    # duplicate guess
    elif guess in guessList:
        print(f'already used this guess. {guess}\nhandling duplicate guess...')
    # correct guess, update hiddenWord, guessList, & numGuesses
    elif guess in word:
        print(f'guess {guess} found in word!\n hiding word')
        guessList.append(guess)
        numGuesses += 1
    # incorrect guess
    else:
        print(f'wrong guess {guess}\nupdating guess list and guesses')
        guessList.append(guess)
        numGuesses+=1

    return hideWord(word, guess)


def hideWord(word, guess) -> str:
    global WIN, STATE
    hiddenWord = ''
    for char in word:
        if char in guessList:
            hiddenWord += char + ' '
        else:
            hiddenWord += '_ '
    print(f'hidden word is {hiddenWord}')
    if '_' not in hiddenWord:
        WIN = True
        STATE = False
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
print('[DONE] server socket successfully closed.')