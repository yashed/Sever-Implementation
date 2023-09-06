import socket

client_socket = socket.socket()

serverAddress = ('localhost', 2728)

client_socket.connect(serverAddress)


name = input("Enter You Name = ")

client_socket.send(bytes(name, 'utf-8'))
print(client_socket.recv(1024).decode())
