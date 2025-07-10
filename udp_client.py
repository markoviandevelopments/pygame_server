import socket
import pickle
import threading
import random

# Client configuration
HOST = '192.168.1.126'  # Server address
SERVER_PORT = 12343   # Server port
CLIENT_PORT = 12346   # Client port
BUFFER_SIZE = 1024

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, CLIENT_PORT))

# Dog class definition
class Dog:
    def __init__(self):
        self.sound = "bow-wow"
        self.breed = "Eastern Pomeranian"
        self.walk = "*truts over to nearest coffee shop*"
        self.x = 13
        self.y = 17

# List of possible dog sounds
DOG_SOUNDS = ["woof", "arf", "yap", "grr", "bow-wow", "ruff"]

def receive_messages():
    print(f"Client listening on {HOST}:{CLIENT_PORT}")
    while True:
        try:
            # Receive Dog object
            data, addr = client_socket.recvfrom(BUFFER_SIZE)
            dog = pickle.loads(data)
            print(f"Received from server {addr}: {dog.__dict__}")
            if dog.sound.lower() == 'exit':
                print("Server sent exit. Closing client.")
                break
        except Exception as e:
            print(f"Error receiving: {e}")
            break
    client_socket.close()

def send_messages():
    dog = Dog()  # Create a Dog instance
    server_address = (HOST, SERVER_PORT)
    while True:
        try:
            # Randomly change the dog's sound
            message = input("Enter a dog sound (or 'exit' to quit, or press Enter for random sound): ").strip()
            if not message:  # If Enter is pressed, choose random sound
                dog.sound = random.choice(DOG_SOUNDS)
            else:
                dog.sound = message
            # Serialize and send Dog object
            data = pickle.dumps(dog)
            client_socket.sendto(data, server_address)
            print(f"Sent to {server_address}: {dog.__dict__}")
            if dog.sound.lower() == 'exit':
                print("Client exiting.")
                break
        except Exception as e:
            print(f"Error sending: {e}")
            break
    client_socket.close()

def main():
    print(f"Starting UDP client on {HOST}:{CLIENT_PORT}")
    # Start threads for receiving and sending
    recv_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)
    recv_thread.start()
    send_thread.start()
    # Wait for threads to finish
    recv_thread.join()
    send_thread.join()
    print("Client closed")

if __name__ == "__main__":
    main()