import socket

class Server:

    def __init__(self,ip='localhost',port=3000):
        self.addr = (ip,port)
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.connection.bind()

        Thread(targert=self.send,args=()).start()
        Thread(targert=self.received,args=()).start()


    def send(self,msg,porta):
        self.msg = msg.encode()
        self.connection.sendto(self.msg, ('localhost',porta))

    def received(self):
        self.connection.recvfrom(1024)
        print(f'Cliente {self.connection[1]} mandou: {self.connection[0].decode()}')