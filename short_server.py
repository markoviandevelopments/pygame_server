# server.py
import socket
import pickle
import threading
import time
import copy
import pygame

BUFFER_SIZE = 256

class O:
    def __init__(self,n=0):
        self.number=n
        self.x = 100
        self.y = 100
        self.moved = False

num = 0

server_socket = socket.socket(2,2)
server_socket.bind(('',9000))

ob = O()

def comm():
    global ob
    print("Server comm thread started, waiting for data...")
    while 1:
        try:
            d, a = server_socket.recvfrom(BUFFER_SIZE)
            print(f"Server received {len(d)} bytes from {a} at {time.time()}")
            o = pickle.loads(d)
            try:
                if ob:
                    if ob.moved:
                        ob.moved = False
                        o = copy.deepcopy(ob)

            except:
                print("ob error/not changed")
                    
            print(f"Server loaded: {o.__dict__}")
            o.number += 1
            ob = copy.deepcopy(o)  # Update global
            serialized = pickle.dumps(o)
            server_socket.sendto(serialized, a)
            print(f"Server sent {len(serialized)} bytes back: {o.__dict__} at {time.time()}")
        except Exception as e:
            print(f"Server error: {e}")
        time.sleep(0.01)


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
            ob.y -= 10
            ob.moved = True
        if keys[pygame.K_a]:
            ob.x -= 10
            ob.moved = True
        if keys[pygame.K_s]:
            ob.y += 10
            ob.moved = True
        if keys[pygame.K_d]:
            ob.x += 10
            ob.moved = True
        
        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 0, 0), (ob.x, ob.y, 50, 50))
        pygame.display.flip()
        print(ob.__dict__)
        time.sleep(.1)
    
    pygame.quit()

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()

