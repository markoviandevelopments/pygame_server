import socket
import pickle

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address
host = '172.20.10.1'
port = 12347
server_address = (host, port)



class Dog():
    def __init__(self):
        Dog.sound = "bark"
        Dog.breed = "German Shepard"
        Dog.walk = "Hello Folks. I am walking!!!"


dog = Dog()


# String to send
message = pickle.dumps(dog)

# Send the string (encode to bytes)
client_socket.sendto(message, server_address)
print(f"Sent to {server_address}: {message}")

# Close socket
client_socket.close()