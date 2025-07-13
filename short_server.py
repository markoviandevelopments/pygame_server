# server.py
import socket
import pickle
import threading
import time
import copy
import pygame
import random

BUFFER_SIZE = 256

class O:
    def __init__(self,n=0):
        self.number=n
        self.x_server = 100
        self.y_server = 100
        self.x_client = 200
        self.y_client = 200
        self.moved = False

num = 0
a = None

server_socket = socket.socket(2,2)
server_socket.bind(('',9000))

ob = O()



def recv():
    global ob
    global a
    print("Server comm thread started, waiting for data...")
    server_socket.settimeout(0.01)
    a = None
    while 1:
        try:
            d, a = server_socket.recvfrom(BUFFER_SIZE)
            print(f"Server received {len(d)} bytes from {a} at {time.time()}")
            o = pickle.loads(d)
            x_server = ob.x_server
            y_server = ob.y_server
            ob = copy.deepcopy(o)
            ob.x_server = x_server
            ob.y_server = y_server
            ob.moved = False
            print(f"Server loaded: {o.__dict__}")
        except Exception as e:
            print(f"Server error: {e}")
        time.sleep(0.1)
        

def send():
    global ob
    global a
    print("Server comm thread started, waiting for data...")
    server_socket.settimeout(0.01)
    
    # d,a = server_socket.recvfrom(BUFFER_SIZE)
    while 1:
        print(ob.__dict__)
        try:
            if a is None: 
                time.sleep(0.1)
                continue
            o = copy.deepcopy(ob)
            o.number += 1
            serialized = pickle.dumps(o)
            server_socket.sendto(serialized, a)
            print(f"Server sent {len(serialized)} bytes back: {o.__dict__} at {time.time()}")
            ob.number = o.number
            
        except Exception as e:
            print(f"Server error: {e}")
        time.sleep(0.1)


def main():
    global ob

    pygame.init()
    window = pygame.display.set_mode((800, 800))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            ob.y_server -= 10
            ob.moved = True
        elif keys[pygame.K_a]:
            ob.x_server -= 10
            ob.moved = True
        elif keys[pygame.K_s]:
            ob.y_server += 10
            ob.moved = True
        elif keys[pygame.K_d]:
            ob.x_server += 10
            ob.moved = True
        else:
            ob.moved = False
        
        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 0, 0), (ob.x_server, ob.y_server, 50, 50))
        pygame.draw.rect(window, (255, 255, 0), (ob.x_client, ob.y_client, 50, 50))
        pygame.display.flip()
        #print(ob.__dict__)
        time.sleep(.1)
    
    pygame.quit()

send_thread = threading.Thread(target=send)
recv_thread = threading.Thread(target=recv)
main_thread = threading.Thread(target=main)

send_thread.start()
recv_thread.start()
main_thread.start()

send_thread.join()
recv_thread.join()
main_thread.join()

