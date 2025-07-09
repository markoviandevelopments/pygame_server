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
        self.sound = "bark"
        self.breed = "German Shepard"
        self.walk = "Hey yous. Eyyyy - I'm walking 'ere!!!"
        self.x = 0
        self.y = 1


dog = Dog()


# String to send
message = pickle.dumps(dog)

# Send the string (encode to bytes)
client_socket.sendto(message, server_address)
print(f"Sent to {server_address}: {message}")

# Close socket
client_socket.close()