import socket
import pickle
import threading
import random

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12343      # Port to bind to
BUFFER_SIZE = 1024

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

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

# Store client address
client_address = None

def receive_messages():
    global client_address
    print(f"UDP server listening on {HOST}:{PORT}")
    while True:
        try:
            # Receive Dog object
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            client_address = addr  # Update client address
            dog = pickle.loads(data)
            print(f"Received from {addr}: {dog.__dict__}")
            if dog.sound.lower() == 'exit':
                print("Client sent exit. Closing server.")
                break
        except Exception as e:
            print(f"Error receiving: {e}")
            break
    server_socket.close()

def send_messages():
    global client_address
    dog = Dog()  # Create a Dog instance
    while True:
        try:
            if client_address:
                # Randomly change the dog's sound
                message = input("Enter a dog sound (or 'exit' to quit, or press Enter for random sound): ").strip()
                if not message:  # If Enter is pressed, choose random sound
                    dog.sound = random.choice(DOG_SOUNDS)
                else:
                    dog.sound = message
                # Serialize and send Dog object
                data = pickle.dumps(dog)
                server_socket.sendto(data, client_address)
                print(f"Sent to {client_address}: {dog.__dict__}")
                if dog.sound.lower() == 'exit':
                    print("Server exiting.")
                    break
            else:
                print("No client connected yet. Waiting...")
                # Wait briefly to avoid spamming the console
                threading.Event().wait(1)
        except Exception as e:
            print(f"Error sending: {e}")
            break
    server_socket.close()

def main():
    # Start threads for receiving and sending
    recv_thread = threading.Thread(target=receive_messages)
    send_thread = threading.Thread(target=send_messages)
    recv_thread.start()
    send_thread.start()
    # Wait for threads to finish
    recv_thread.join()
    send_thread.join()
    print("Server closed")

if __name__ == "__main__":
    main()