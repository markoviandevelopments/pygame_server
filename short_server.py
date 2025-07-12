# server.py
import socket
import pickle
import threading
import time

class O:
    def __init__(self,n=0):
        self.number=n

num = 0

server_socket = socket.socket(2,2)
server_socket.bind(('',9000))

def comm():
    global num
    while 1:
        d,a = server_socket.recvfrom(99)
        o = pickle.loads(d)
        o.number += 1
        server_socket.sendto(pickle.dumps(o),a)
        #print(f"{o.__dict__}")
        num = o.number


def main():
    global num
    while 1:
        print(num)
        time.sleep(1)

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()

