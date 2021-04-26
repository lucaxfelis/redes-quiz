import socket
from threading import Thread

class Client:

    def __init__(self,ip='localhost',port=3000):
        self.addr= (ip,port)
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.connection.bind()

        Thread(target=self.received(),args=()).start()

        while True:
            self.msg = input('digite sua mensagem:')
            self.connection.sendto(self.msg.decode(), self.addr)

    
    def received (self):
        while True:
            self.connection.recvfrom(1024)
            print(f'servidor mandou: {self.connection[0].decode()}')
