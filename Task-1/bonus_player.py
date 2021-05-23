port = 5555     #should be unique; so keep changing if it says "Already in use"

import socket

player = socket.socket()

player.connect(('localhost',port))
print('Connection established...')

cards = []
no_of_rounds = int(player.recv(1024).decode())

while True:
    for j in range(no_of_rounds):
        cards_string = player.recv(1024).decode()
        cards = cards_string.split()
        for i in range(len(cards)):
            cards[i] = int(cards[i])
          
        print(f'Round-{j+1}: {cards}')

        #scaling the cards by 13
        for ind,card in enumerate(cards):
            cards[ind] = cards[ind] % 13
            if cards[ind] == 0:
                cards[ind] = 13
            
        player.send(str(max(cards)).encode())

        cards.clear()

    print(player.recv(1024).decode())

    char = player.recv(1024).decode()
    if(char == 'N'):
        break
