port = 5556     #should be unique; so keep changing if it says "Already in use"

import socket

client = socket.socket()

client.connect(('localhost',port))
print('Connection established...')

t = int(client.recv(1024).decode())
print(t)

for i in range(t):
    print('Input line-' + str(i+1) +':')
    cars = input()

    client.send(str(cars).encode())


client.close()
