import socket
import pickle

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and port
host = '0.0.0.0'
port = 12349
server_socket.bind((host, port))


class Dog():
    def __init__(self):
        Dog.sound = "bark"
        Dog.breed = "German Shepard"
        Dog.walk = "Hello Folks. I am walking!!!"



print(f"UDP server listening on {host}:{port}")

# Receive data
while True:
    data, addr = server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
    dog = pickle.loads(data)  # Decode bytes to string
    print(f"Received from {addr}: {dog.walk}")

# Close socket
server_socket.close()