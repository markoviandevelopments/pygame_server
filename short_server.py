# server.py
import socket
import pickle
import threading
import time
import copy
import pygame

BUFFER_SIZE = 1024

class O:
    def __init__(self,n=0):
        self.number=n
        self.x = 100
        self.y = 100

num = 0

server_socket = socket.socket(2,2)
server_socket.bind(('',9000))

ob = O()

def comm():
    global ob
    while 1:
        try:
            if not ob:
                o = copy.deepcopy(ob)
        except:
            print("O is empty or being altered")
        d,a = server_socket.recvfrom(BUFFER_SIZE)
        o = pickle.loads(d)
        o.number += 1
        server_socket.sendto(pickle.dumps(o),a)
        #print(f"{o.__dict__}")
        ob = copy.deepcopy(o)
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
        if keys[pygame.K_a]:
            ob.x -= 10
        if keys[pygame.K_s]:
            ob.y += 10
        if keys[pygame.K_d]:
            ob.x += 10
        
        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 0, 0), (ob.x, ob.y, 50, 50))
        pygame.display.flip()
        print(ob.number)
        time.sleep(.1)
    
    pygame.quit()

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()

