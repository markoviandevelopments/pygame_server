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
port = 12346

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
server_socket.setblocking(False)
print(f"Server listening on {host}:{port}")

# List to keep track of client connections
clients = []

client_coords = []

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
                    client_coords.append([random.randint(100, 700), random.randint(100, 700)])
                    print(f"New connection from {client_address}")
                except socket.error as e:
                    print(f"Error accepting connection: {e}")

        # Handle readable client sockets
        try:
            for i, sock in enumerate(readable):
                if sock in clients:
                    try:
                        data = sock.recv(1024)
                        if data:
                            received_number = data.decode()
                            print(f"Received from {sock.getpeername()}: {received_number}")
                            move = int(received_number)
                            if move == 1:
                                client_coords[i][0] += 50
                            elif move == 2:
                                client_coords[i][1] -= 50
                            elif move == 3:
                                client_coords[i][0] -= 50
                            elif move == 4:
                                client_coords[i][1] += 50

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
        except:
            print("oops")

        # Send random number to all connected clients
        for i, client in enumerate(writable[:]):  # Use copy to avoid modification during iteration
            try:
                client.send(str([i, client_coords]).encode())
                print(f"Sent to {client.getpeername()}:  {str([i, client_coords])} CLients: {clients}")
            except socket.error as e:
                if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    try:
                        print(f"Client {client.getpeername()} disconnected or error: {e}")
                    except socket.error:
                        print("Client disconnected or error")
                    clients.remove(client)
                    client.close()

        time.sleep(.1)  # Control the rate of sending numbers

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    for client in clients:
        client.close()
    server_socket.close()