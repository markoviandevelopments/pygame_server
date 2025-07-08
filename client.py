import socket
import random
import time
import select
import errno

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)

# Define host and port
host = '192.168.1.126'
port = 12345

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
    while True:
        # Check for readable or writable socket
        readable, writable, _ = select.select([client_socket], [client_socket], [], 1.0)

        # Handle receiving data
        if readable:
            try:
                data = client_socket.recv(1024)
                if data:
                    received_number = data.decode()
                    print(f"Received from server: {received_number}")
                else:
                    print("Server disconnected")
                    break
            except socket.error as e:
                if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    print(f"Receive error: {e}")
                    break

        # Send random number to server
        if writable:
            try:
                random_number = random.randint(1, 100)
                client_socket.send(str(random_number).encode())
                print(f"Sent to server: {random_number}")
            except socket.error as e:
                if e.errno not in [errno.EAGAIN, errno.EWOULDBLOCK]:
                    print(f"Send error: {e}")
                    break

        time.sleep(1)  # Control the rate of sending numbers

except KeyboardInterrupt:
    print("\nDisconnecting from server...")
finally:
    client_socket.close()