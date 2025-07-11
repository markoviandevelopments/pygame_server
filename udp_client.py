import socket
import pickle
import threading
import random
import time

# Client configuration
HOST = '192.168.1.126'  # Server address
SERVER_PORT = 12333   # Server port
CLIENT_PORT = 12336   # Client port
BUFFER_SIZE = 512

time_ref = time.time()

# Create UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, CLIENT_PORT))

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



def receive_messages():
    global shared_dog
    print(f"Client listening on {HOST}:{CLIENT_PORT}")
    while True:
        try:
            # Receive Dog object
            data, addr = client_socket.recvfrom(BUFFER_SIZE)
            received_dog = pickle.loads(data)
            
            with dog_lock:
                # Update shared_dog with received attributes
                shared_dog.sound = received_dog.sound
                shared_dog.number = received_dog.number
                shared_dog.last_modified_by = received_dog.last_modified_by
                shared_dog.just_modified = received_dog.just_modified
                # Increment
                if shared_dog.number % 2 == 0 and shared_dog.last_modified_by == "server":
                    #print(f"Received from server {addr}: {received_dog.__dict__}")
                    shared_dog.number += 1
                    shared_dog.last_modified_by = "client"
                    shared_dog.just_modified = True

        except Exception as e:
            print(f"Error receiving: {e}")
            break
    client_socket.close()

def send_messages():
    global shared_dog
    global time_ref
    server_address = (HOST, SERVER_PORT)
    client_socket.connect(server_address)
    while True:
        try:
            with dog_lock:
                    # Randomly change the dog's sound
                    shared_dog.sound = random.choice(DOG_SOUNDS)
                    # Serialize and send Dog object
                    data = pickle.dumps(shared_dog)
                    client_socket.send(data)
                    if shared_dog.last_modified_by == "client" and shared_dog.just_modified:
                        time_el = shared_dog.number / (time.time() - time_ref)
                        if shared_dog.number > 0:
                            avg_time = 1 / time_el
                        else:
                            avg_time = 0
                        print(f"Sent to {server_address}: {shared_dog.__dict__} freq: {time_el} Avg time {avg_time}")
                        shared_dog.just_modified = False
        except Exception as e:
            print(f"Error sending: {e}")
            break
        #time.sleep(3)
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