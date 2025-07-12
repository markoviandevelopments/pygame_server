# client.py
import socket
import pickle
import threading
import pygame
import time
import copy

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
    try:
        # Initial send to break deadlock
        o.number += 1
        serialized = pickle.dumps(o)
        client_socket.sendto(serialized, a)
        print(f"Client sent initial {len(serialized)} bytes: {o.__dict__} at {time.time()}")
    except Exception as e:
        print(f"Client initial send error: {e}")
    while 1:
        try:
            d, addr = client_socket.recvfrom(BUFFER_SIZE)
            print(f"Client received {len(d)} bytes from {addr} at {time.time()}")
            ob = pickle.loads(d)
            try:
                if o:
                    if o.moved:
                        o.moved = False
                        ob = copy.deepcopy(o)

            except:
                print("ob error/not changed")
            print(f"Client loaded: {ob.__dict__}")
            ob.number += 1
            o = copy.deepcopy(ob)  # Update global
            serialized = pickle.dumps(ob)
            client_socket.sendto(serialized, a)
            print(f"Client sent {len(serialized)} bytes: {ob.__dict__} at {time.time()}")
        except Exception as e:
            print(f"Client error: {e}")
        time.sleep(.01)

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
        if keys[pygame.K_a]:
            o.x -= 10
            o.moved = True
        if keys[pygame.K_s]:
            o.y += 10
            o.moved = True
        if keys[pygame.K_d]:
            o.x += 10
            o.moved = True

        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 255, 0), (o.x, o.y, 50, 50))
        pygame.display.flip()
        print(o.__dict__)
        time.sleep(.1)

    pygame.quit()

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()
