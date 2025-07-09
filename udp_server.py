import socket
import pickle

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and port
host = '0.0.0.0'
port = 12343
server_socket.bind((host, port))

print(f"UDP server listening on {host}:{port}")

class Dog():
    def __init__(self):
        self.sound = "bark"
        self.breed = "German Shepard"
        self.walk = "Hey yous. Eyyyy - I'm walking 'ere!!!"
        self.x = 0
        self.y = 1

dog = Dog()

# Receive data
while True:
    data, addr = server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
    dog = pickle.loads(data)  # Decode bytes to string
    print(f"Received from {addr}: {dog.__dict__}")

# Close socket
server_socket.close()