port = 5555      #should be unique; so keep changing if it says "Already in use"

import socket
import threading
import random
import time

casino = socket.socket()
casino.bind(('localhost',port))

casino.listen(1)
print('Waiting for the client!')

client, addr = casino.accept()
print('Connected with client...' + addr[0] + "  " + str(addr[1]))

initialize = client.recv(1024).decode()   #recv both data at once
initialize = initialize.split()

no_of_players = int(initialize[0])
no_of_rounds = int(initialize[1])

print("Welcome to the game! \nNo. of players = %d \nNo. of rounds in a game = %d\n" % (no_of_players,no_of_rounds))

client.close()

#to store the details of player sockets
players = []
address = []

casino.listen(no_of_players)
#casino.listen(100)
print("Waiting for players!")

No_of_win = []          #no of rounds won by each player
for _ in range(no_of_players):
    No_of_win.append(0)

#to get the cards returned by each player
return_cards = []
def return_card():
    for player in players:
        return_cards.append(int(player.recv(1024).decode()))
        #time.sleep(0.2)
    print(return_cards)

def winner():
    max_value = max(return_cards)
    max_index = []         #list cause can be more than one -> draw
    for ind,card in enumerate(return_cards):
        if card == max_value:
            max_index.append(ind)
    return max_index


#to distribute 3cards to each player
def distr_cards(n,cards):
    player = players[n]
    send_list = ''       #sending list as string
    for i in range(3):
        send_list += str(cards[3*n+i]) + ' '
    player.send(str(send_list).encode())

#for printing final winner at every player's terminal
def send_msg(msg):
    for player in players:
        player.send(str(msg).encode())


for _ in range(no_of_players):
    player, addr = casino.accept()
    print('Connected with ' + addr[0] + "  " + str(addr[1]))
    player.send(str(no_of_rounds).encode())

    players.append(player)
    address.append(addr)

while True:
    for j in range(no_of_rounds):

        #generating 3times total player cards
        cards = random.sample(range(1,53),3*no_of_players)
        print(f"ROUND-{j+1}")
        print(cards)

        threads = []
        for i in range(no_of_players):
            t = threading.Thread(target=distr_cards, args=(i,cards))
            threads.append(t)
            t.start()
            #time.sleep(0.1)

        for t in threads:
            t.join()

        return_card()

        win_ind = []   #wining indices
        win_ind = winner()        #func to findout player having max cards out of returned

        if len(win_ind) == 1:
            ind = win_ind.pop()
            No_of_win[ind] += 1
            print(f'Player-{ind+1} is the winner of Round {j+1}')
        else:
            msg = "In Round %d, There is a tie b/w: "
            for ind in win_ind:
                msg += ("Player-%d," %(ind+1))
                No_of_win[ind] += 1
            print(msg)
        
        #clearing lists(data) so that can be used for next round
        cards.clear()
        return_cards.clear()

    #finding overall winner
    max_value = max(No_of_win)
    max_ind = []      #as can be more than one -> draw

    for ind,wins in enumerate(No_of_win):
        if wins == max_value:
            max_ind.append(ind)

    if len(max_ind) == 1:
        ind = max_ind.pop()
        msg = "Player-%d wins the game" % (ind+1)
        print(msg)
    else:
        winners = ""
        for ind in max_ind:
            winners += ("Player-%d, " %(ind+1))
        msg = ("The game tied b/w:  " + winners)
        print(msg)

    send_msg(msg)

    char = input("Do you want to play again? (Y/N): ")
    send_msg(char)

    if(char == 'N'):
        print('Thanks for playing! Exitting...')
        break
