# server.py
import socket,pickle
class O:
 def __init__(self,n=0):self.number=n
k=socket.socket(2,2)
k.bind(('',9000))
while 1:
    d,a=k.recvfrom(99)
    o=pickle.loads(d)
    o.number+=1
    k.sendto(pickle.dumps(o),a)
    print(f"{o.__dict__}")