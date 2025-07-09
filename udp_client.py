import socket
import pickle

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
host = '172.20.10.2'
port = 12343
server_address = (host, port)



class Dog():
    def __init__(self):
        self.sound = "bow-wow"
        self.breed = "Eastern Pomeranian"
        self.walk = "*truts over to nearest coffee shop*"
        self.x = 13
        self.y = 17

dog = Dog()


# String to send


# Send the string (encode to bytes)
while True:
    dog.sound = input()
    message = pickle.dumps(dog)
    client_socket.sendto(message, server_address)
    print(f"Sent to {server_address}: {message}")

# Close socket
client_socket.close()