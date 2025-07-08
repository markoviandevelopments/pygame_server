import socket
import random
import time
import select
import errno

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Define host and port
host = '0.0.0.0'
port = 12345

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
server_socket.setblocking(False)
print(f"Server listening on {host}:{port}")

# List to keep track of client connections
clients = []

try:
    while True:
        # Check for new connections or readable sockets
        readable, writable, _ = select.select([server_socket] + clients, clients, [], 1.0)

        # Handle new connections
        for sock in readable:
            if sock is server_socket:
                try:
                    client_socket, client_address = server_socket.accept()
                    client_socket.setblocking(False)
                    clients.append(client_socket)
                    print(f"New connection from {client_address}")
                except socket.error as e:
                    print(f"Error accepting connection: {e}")

        # Handle readable client sockets
        for sock in readable:
            if sock in clients:
                try:
                    data = sock.recv(1024)
                    if data:
                        received_number = data.decode()
                        print(f"Received from {sock.getpeername()}: {received_number}")
                    else:
                        # Client disconnected
                        print(f"Client {sock.getpeername()} disconnected")
                        clients.remove(sock)
                        sock.close()
                except socket.error as e:
                    if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                        print(f"Client {sock.getpeername()} error: {e}")
                        clients.remove(sock)
                        sock.close()

        # Send random number to all connected clients
        for client in writable[:]:  # Use copy to avoid modification during iteration
            try:
                random_number = random.randint(1, 100)
                client.send(str(random_number).encode())
                print(f"Sent to {client.getpeername()}: {random_number}")
            except socket.error as e:
                if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    try:
                        print(f"Client {client.getpeername()} disconnected or error: {e}")
                    except socket.error:
                        print("Client disconnected or error")
                    clients.remove(client)
                    client.close()

        time.sleep(1)  # Control the rate of sending numbers

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    for client in clients:
        client.close()
    server_socket.close()