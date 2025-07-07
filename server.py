import socket
import random

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host and port
host = '0.0.0.0'  # localhost
port = 12345

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Generate random number
    random_number = random.randint(1, 100)
    
    # Send random number to client
    client_socket.send(str(random_number).encode())
    print(f"Sent random number: {random_number}")

    # Close client socket
    client_socket.close()
    
# Close server socket (unreachable in this example)
server_socket.close()
