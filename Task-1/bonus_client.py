port = 5555      #should be unique; so keep changing if it says "Already in use"

import socket
import time

client = socket.socket()

client.connect(('localhost',port))
print('Connection established...')

no_of_players = input("Enter number of Players: ")

while True:
    no_of_rounds = input("Enter number of round for a game: ")
    if int(no_of_rounds) % int(no_of_players) != 0:
        break
    print("No. of Rounds shouldn't be divisible by No. of players! Enter again...")

initialize = str(no_of_players) + ' ' + str(no_of_rounds)   #will send both the data together
client.send(str(initialize).encode())

client.close()