port = 5555      #should be unique; so keep changing if it says "Already in use"

import socket
import threading
import random

casino = socket.socket()
casino.bind(('localhost',port))

casino.listen(3)
print('Waiting for players!')

#to store the details of player sockets
players = []
address = []

No_of_Rounds = 4
No_of_win = [0,0,0]   #no of rounds each player win

#to get the cards returned by each player
return_cards = []
def return_card():
    for player in players:
        return_cards.append(int(player.recv(1024).decode()))
        #return_cards.append(int(player.recv(1024).decode()))
        #return_cards.append((int)(player.recv(1024).decode()))
    print(return_cards)

def winner():
    max_value = max(return_cards)
    max_index = []   #can be more than one -> draw
    for ind,card in enumerate(return_cards):
        if card == max_value:
            max_index.append(ind)
    return max_index


def distr_card(n,cards):
    player = players[n]
    send_list = ''       #sending list as string
    for i in range(3):
        send_list += str(cards[3*n+i]) + ' '
    player.send(str(send_list).encode())

#for printing final winner at every player's terminal
def send_msg(msg):
    for player in players:
        player.send(str(msg).encode())

for _ in range(3):
    player, addr = casino.accept()
    print('Connected with ' + addr[0] + "  " + str(addr[1]))

    players.append(player)
    address.append(addr)
while True:
    for j in range(No_of_Rounds):

        #generating 9 cards
        cards = random.sample(range(1,53),9)
        print(f"ROUND-{j+1}")
        print(cards)

        t1 = threading.Thread(target=distr_card,args= (0,cards))
        t2 = threading.Thread(target=distr_card,args= (1,cards))
        t3 = threading.Thread(target=distr_card,args= (2,cards))

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        return_card()

        win_ind = []   #wining indices
        win_ind = winner()
        if len(win_ind) == 1:
            ind = win_ind.pop()
            No_of_win[ind] += 1
            print(f'Player-{ind+1} is the winner of Round {j+1}')
        elif len(win_ind) == 2:
            ind1 = win_ind.pop()
            ind2 = win_ind.pop()
            No_of_win[ind1] += 1
            No_of_win[ind2] += 1
            print(f'There is a tie b/w Player-{ind1+1} & Player-{ind2+1} in Round {j+1}')
        else:
            for ind,wins in enumerate(No_of_win):
                No_of_win[ind] += 1
            print(f'There is a tie b/w all the players in Round {j+1}')
            
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
    elif len(max_ind) == 2:
        ind1 = max_ind.pop()
        ind2 = max_ind.pop()
        msg = "Tie b/w Player-%d & Player-%d in the game." % (ind1+1,ind2+1)
        print(msg)
    else:
        msg = "Noone wins the game; TIE"
        print(msg)
    
    send_msg(msg)

    char = input("Do you want to play again? (Y/N): ")
    send_msg(char)

    if(char == 'N'):
        print('Thanks for playing! Exitting...')
        break
        