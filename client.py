import time
import sys
from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR, timeout
from threading import Thread

class Client:

    def __init__(self,ip='localhost', server_port=3000):
        server_addr = (ip, server_port)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.__running = False

        print("# # # SEJA BEM-VINDO AO QUIZ RACHA-CUCA # # #\n")
        print("@ para jogar, digite 'jogar'")

        Thread(target=self.receiving ,args=()).start()
        try:
            while True:
                msg = input('')
                self.socket.sendto(msg.encode(), server_addr)
        except(KeyboardInterrupt, SystemExit):
            self.__running = False
        
        self.socket.close()
    
    def receiving(self):
        self.__running = True

        while self.__running:
            try:
                response_msg, client_addr = self.socket.recvfrom(1024)
                print(response_msg.decode())
                print()
            except:
                self.__running = False
                break

Client()