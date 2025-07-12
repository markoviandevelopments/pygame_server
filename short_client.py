# client.py
import socket
import pickle
import threading
import time

class O:
    def __init__(self,n=0):
        self.number=n

client_socket = socket.socket(2,2)
a=('192.168.1.126',9000)
o=O()

def comm():
    global o
    while 1:
        o.number += 1
        client_socket.sendto(pickle.dumps(o),a)
        d , _ = client_socket.recvfrom(99)
        o = pickle.loads(d)
        # print(f"{o.__dict__}")

def main():
    global o
    while 1:
        print(o.number)
        time.sleep(1)

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()
