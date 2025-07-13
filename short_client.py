# client.py
import socket
import pickle
import threading
import pygame
import time
import copy
import random

BUFFER_SIZE = 256

class O:
    def __init__(self,n=0):
        self.number=n
        self.x = 100
        self.y = 100
        self.moved = False

client_socket = socket.socket(2,2)
a = ('192.168.1.126',9000)
o = O()

def comm():
    global o
    print("Client comm thread started")
    client_socket.settimeout(0.1)
    try:
        # Initial send to break deadlock
        o.number += 1
        serialized = pickle.dumps(o)
        client_socket.sendto(serialized, a)
        print(f"Client sent initial {len(serialized)} bytes: {o.__dict__} at {time.time()}")
    except Exception as e:
        print(f"Client initial send error: {e}")
    
    while 1:
        print(o.__dict__)
        try:
            if o.moved:
                print("Moved")
                ob = copy.deepcopy(o)
                ob.number += 1
                serialized = pickle.dumps(ob)
                client_socket.sendto(serialized, a)
                print(f"Client sent {len(serialized)} bytes: {ob.__dict__} at {time.time()}")
                o.moved = False
                o.number = ob.number
            else:
                try:
                    d, addr = client_socket.recvfrom(BUFFER_SIZE)
                    print(f"Client received {len(d)} bytes from {addr} at {time.time()}")
                    ob = pickle.loads(d)
                    if ob.number > o.number:
                            o = copy.deepcopy(ob)
                            o.moved = False
                            print(f"Client loaded: {ob.__dict__}")
                except socket.timeout:
                    pass

        except Exception as e:
            print(f"Client error: {e}")
        time.sleep(.1)

def main():
    global o

    pygame.init()
    window = pygame.display.set_mode((800, 800))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            o.y -= 10
            o.moved = True
        elif keys[pygame.K_a]:
            o.x -= 10
            o.moved = True
        elif keys[pygame.K_s]:
            o.y += 10
            o.moved = True
        elif keys[pygame.K_d]:
            o.x += 10
            o.moved = True
        else:
            o.moved = False

        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 255, 0), (o.x, o.y, 50, 50))
        pygame.display.flip()
        #print(o.__dict__)
        time.sleep(.1)

    pygame.quit()

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()
