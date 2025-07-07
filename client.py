import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host and port
host = '192.168.1.126'  # localhost
port = 12345

try:
    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Receive data from server
    data = client_socket.recv(1024)
    print(f"Received random number: {data.decode()}")

except ConnectionRefusedError:
    print("Error: Server is not running or connection was refused")

finally:
    # Close the socket
    client_socket.close()
