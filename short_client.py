# client.py
import socket
import pickle
import threading
import pygame
import time
import copy

BUFFER_SIZE = 1024

class O:
    def __init__(self,n=0):
        self.number=n
        self.x = 100
        self.y = 100

client_socket = socket.socket(2,2)
a=('192.168.1.126',9000)
o=O()

def comm():
    global o
    while 1:
        # try:
        #     if not o:
        #         ob = copy.deepcopy(o)
        # except:
        #     print("O is empty or being altered")
        d, a = client_socket.recvfrom(BUFFER_SIZE)
        ob = pickle.loads(d)
        ob.number += 1
        client_socket.sendto(pickle.dumps(ob),a)
        o = copy.deepcopy(ob)
        # print(f"{o.__dict__}")
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
        if keys[pygame.K_a]:
            o.x -= 10
        if keys[pygame.K_s]:
            o.y += 10
        if keys[pygame.K_d]:
            o.x += 10

        window.fill((0,0,0))
        pygame.draw.rect(window, (255, 255, 0), (o.x, o.y, 50, 50))
        pygame.display.flip()
        print(o.number)
        time.sleep(.1)

    pygame.quit()

comm_thread = threading.Thread(target=comm)
main_thread = threading.Thread(target=main)

comm_thread.start()
main_thread.start()

comm_thread.join()
main_thread.join()
