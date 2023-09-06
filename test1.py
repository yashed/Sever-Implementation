import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

while True:
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Handle the client's request here

    client_socket.close()
