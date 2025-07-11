import socket
import pickle
import threading
import random
import time

# Server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12333      # Port to bind to
BUFFER_SIZE = 512

# Create UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

# Dog class definition
class Dog:
    def __init__(self):
        self.sound = "bow-wow"
        self.number = 0
        self.last_modified_by = "server"
        self.just_modified = False

# List of possible dog sounds
DOG_SOUNDS = [
    "woof", "arf", "yap", "grr", "bow-wow", "ruff", "bark", "howl", "whine", "growl",
    "yowl", "yelp", "snarl", "chuff", "woof-woof", "awoo", "grumble", "mutt-mutt", "huff", "pant",
    "meow", "oink", "moo", "beep-boop", "yodel", "honk", "screech", "vroom", "quack", "ribbit",
    "boing", "zap", "whoop", "gobble", "tweet", "ding-dong", "la-la-la", "whirrr", "psst", "eek"
]


shared_dog = Dog()
dog_lock = threading.Lock()


# Store client address
client_address = None

def receive_messages():
    global client_address
    global shared_dog
    print(f"UDP server listening on {HOST}:{PORT}")
    while True:
        try:
            # Receive Dog object
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            client_address = addr  # Update client address
            received_dog = pickle.loads(data)
            with dog_lock:
                # Update shared_dog with received attributes
                shared_dog.sound = received_dog.sound
                shared_dog.number = received_dog.number
                shared_dog.last_modified_by = received_dog.last_modified_by
                shared_dog.just_modified = received_dog.just_modified
                # Increment number if even
                #print(f"Received from {addr}: {received_dog.__dict__}")
                if shared_dog.number % 2 > 0 and shared_dog.last_modified_by == "client":
                    #print(f"Received from {addr}: {received_dog.__dict__}")
                    shared_dog.number += 1
                    shared_dog.last_modified_by = "server"
                    shared_dog.just_modified = True


        except Exception as e:
            print(f"Error receiving: {e}")
            break
    server_socket.close()

def send_messages():
    global client_address
    global shared_dog
    while True:
        try:
            if client_address:
                with dog_lock:
                    # Randomly change the dog's sound
                    shared_dog.sound = random.choice(DOG_SOUNDS)
                    # Serialize and send Dog object
                    data = pickle.dumps(shared_dog)
                    
                    if shared_dog.last_modified_by == "server" and shared_dog.just_modified:
                        server_socket.sendto(data, client_address)
                        print(f"Sent to {client_address}: {shared_dog.__dict__}")
                        shared_dog.just_modified = False
            else:
                print("No client connected yet. Waiting...")
                # Wait briefly to avoid spamming the console
                #threading.Event().wait(1)
        except Exception as e:
            print(f"Error sending: {e}")
            break
        #time.sleep(3)
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