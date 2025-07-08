import socket
import random
import time
import select
import errno
import pygame
import ast

pygame.init()

window = pygame.display.set_mode((800, 800))

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)

# Define host and port
host = '192.168.1.126'
port = 12346

coords = [[0, 0]]


# Attempt to connect with retry for non-blocking
connected = False
while not connected:
    try:
        client_socket.connect((host, port))
        connected = True
        print(f"Connected to server at {host}:{port}")
    except socket.error as e:
        if e.errno == errno.EINPROGRESS:
            # Connection is in progress, wait briefly and check again
            time.sleep(0.1)
            readable, writable, _ = select.select([], [client_socket], [], 0)
            if client_socket in writable:
                # Check if connection was successful
                error = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                if error == 0:
                    connected = True
                    print(f"Connected to server at {host}:{port}")
                else:
                    print(f"Connection failed: {error}")
                    client_socket.close()
                    exit(1)
        elif e.errno == errno.ECONNREFUSED:
            print("Error: Server is not running or connection was refused")
            client_socket.close()
            exit(1)
        else:
            print(f"Connection error: {e}")
            client_socket.close()
            exit(1)

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        move = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            move = 1
        if keys[pygame.K_w]:
            move = 2
        if keys[pygame.K_a]:
            move = 3
        if keys[pygame.K_s]:
            move = 4
        
        # Check for readable or writable socket
        readable, writable, _ = select.select([client_socket], [client_socket], [], 1.0)

        # Handle receiving data
        try:
            if readable:
                try:
                    data = client_socket.recv(1024)
                    if data:
                        coords = ast.literal_eval(data.decode())
                        print(f"Received from server: {coords} Number of clients: {len(coords[1])}")
                        window.fill((0,0,0))
                        for i in range(len(coords[1])):
                            x = coords[1][i][0]
                            y = coords[1][i][1]
                            pygame.draw.rect(window, (255, 0, 0), (x, y, 50, 50))
                        pygame.display.flip()
                    else:
                        print("Server disconnected")
                        break
                except socket.error as e:
                    if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                        print(f"Receive error: {e}")
                        break
        except:
            print("oops")

        # Send number to server
        if writable:
            try:
                client_socket.send(str(move).encode())
                print(f"Sent to server: {move}")
            except socket.error as e:
                if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    print(f"Send error: {e}")
                    break

        time.sleep(.1)  # Control the rate of sending numbers

except KeyboardInterrupt:
    print("\nDisconnecting from server...")
    pygame.quit()
finally:
    client_socket.close()
    pygame.quit()
pygame.quit()