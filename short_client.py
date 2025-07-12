# client.py
import socket
import pickle
import threading

class O:
    def __init__(self,n=0):
        self.number=n

client_socket = socket.socket(2,2)
a=('192.168.1.126',9000)
o=O()

while 1:
    o.number += 1
    client_socket.sendto(pickle.dumps(o),a)
    d , _ = client_socket.recvfrom(99)
    o = pickle.loads(d)
    print(f"{o.__dict__}")