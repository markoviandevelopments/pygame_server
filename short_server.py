# server.py
import socket
import pickle
import threading

class O:
    def __init__(self,n=0):
        self.number=n

server_socket = socket.socket(2,2)
server_socket.bind(('',9000))

while 1:
    d,a=server_socket.recvfrom(99)
    o=pickle.loads(d)
    o.number+=1
    server_socket.sendto(pickle.dumps(o),a)
    print(f"{o.__dict__}")