import socket
import random
import time
import select

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(False)

# Define host and port
host = '192.168.1.126'
port = 12345

try:
    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    while True:
        # Check for readable socket
        readable, _, _ = select.select([client_socket], [], [], 1.0)

        if readable:
            try:
                # Receive data from server
                data = client_socket.recv(1024)
                if data:
                    received_number = data.decode()
                    print(f"Received from server: {received_number}")
                else:
                    print("Server disconnected")
                    break
            except socket.error:
                pass

        # Send random number to server every second
        try:
            random_number = random.randint(1, 100)
            client_socket.send(str(random_number).encode())
            print(f"Sent to server: {random_number}")
        except socket.error:
            print("Server disconnected")
            break

        time.sleep(1)  # Control the rate of sending numbers

except ConnectionRefusedError:
    print("Error: Server is not running or connection was refused")
except KeyboardInterrupt:
    print("\nDisconnecting from server...")
finally:
    client_socket.close()
