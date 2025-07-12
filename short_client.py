# client.py
import socket,pickle,sys
class O:
 def __init__(self,n=0):self.number=n
k=socket.socket(2,2)
a=('192.168.1.126',9000)
o=O()
while 1:
    o.number+=1
    k.sendto(pickle.dumps(o),a)
    d,_=k.recvfrom(99)
    o=pickle.loads(d)