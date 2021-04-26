import socket
from threading import Thread

class Client:

    def __init__(self,ip='localhost',port=3000):
        self.addr= (ip,port)
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #self.connection.bind()

        Thread(target=self.received,args=()).start()
        print("# # # SEJA BEM-VINDO AO QUIZ RACHA-CUCA # # #\n")
        print("@ para jogar, digite 'jogar'")

        while True:
            self.msg = input('\n> ')
            self.connection.sendto(self.msg.encode(), self.addr)
    
    def received(self):
        while True:
            resposta = self.connection.recvfrom(1024)
            print(f'servidor mandou: {resposta[0].decode()}')

c = Client()