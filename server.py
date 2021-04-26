import socket
import time
from threading import Thread
from quiz import *

class Server:

    def __init__(self,ip='localhost',port=3000):
        self.addr = (ip,port)
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.connection.bind(self.addr)

        #Thread(target=self.send,args=()).start()
        #Thread(target=self.received,args=()).start()
  
    def send(self,msg,porta):
        self.msg = msg.encode()
        self.connection.sendto(self.msg, ('localhost',porta))

    def receive_playe(self):
        while True:
            resposta = self.connection.recvfrom(1024)
            print(f'Cliente {resposta[1]} mandou: {resposta[0].decode()}')

class Room:

    def __init__(self):
        self.lista = []
        self.players_num = 2
        self.server = Server()
        self.receive_players()
        #Thread(target=self.receive_players, args=()).start()
        #Thread(target=self.start_game, args=()).start()

    def receive_players(self):
        while len(self.lista) < self.players_num:
            resposta = self.server.connection.recvfrom(1024)
            client_res = resposta[0].decode()
            client_addr = resposta[1][1]  
            if client_res == 'jogar' and client_addr not in self.lista:
                self.server.send('Entrou na sala!', client_addr)
                self.lista.append(client_addr)
                self.server.send(f'Você é o jogador {self.lista.index(client_addr) + 1}', client_addr)
        
        self.broadcast("Jogo começará em breve. Se prepare!")
        time.sleep(3)
        self.placar = {str(k):0 for k in self.lista}
        self.start_game()

    def start_game(self):
        print("A partida começou!\n")
        quiz = Quiz(questions_num = 3)
        numero_rodadas = quiz.questions_num
        for rodada in range(numero_rodadas):
            pergunta, resposta = quiz.get_question()
            #Thread(target=self.game_timer, args=()).start()
            self.broadcast(pergunta)
            respondeu = {str(k):-1 for k in self.lista}
            timeout = time.time() + 10
            self.listen(resposta, respondeu, timeout)
        #Thread(target=self.game_timer, args=()).stop()
        print('parou')
        print("placar", self.print_ranking())

    def broadcast(self, msg):
        for addr in self.lista:
            self.server.send(msg, addr)

    def countdown(self):
        global my_timer

        my_timer = 5

        for x in range(5):
            my_timer = my_timer - 1
            time.sleep(1)    
        
    def listen(self, resposta, respondeu, timeout):
        
        nao_acertou = True
        no_limite = True
        countdown_t = Thread(target=self.countdown, args=())
        countdown_t.start()

        while no_limite and nao_acertou:
            no_limite = time.time() < timeout
            print('parou')
            recebido = self.server.connection.recvfrom(1024)
            print('alguem respondeu')
            palpite = recebido[0].decode()
            client_addr = recebido[1][1]
            respondeu[str(client_addr)] = 0
            print(resposta, palpite)
            if palpite == resposta:
                self.server.send("acertou", client_addr)
                self.placar[str(client_addr)] += 25
                nao_acertou = False
                
            elif palpite != resposta:
                self.server.send("eroooou", client_addr)
                self.placar[str(client_addr)] -= 5
        
        print("quem respondeu", respondeu)
        for key in self.placar.keys():
            self.placar[key] += respondeu[key]
        
        return

    import time
timeout = time.time() + 6   # 5 minutes from now
while True:
    test = 0
    if test == 5 or time.time() > timeout:
        break
    test = test - 1


    def game_timer(self):
        time.sleep(5)
        print('acabou o tempo')

    def print_ranking(self):
        self.ranking = [(k, v) for k,v in self.placar.items()]
        self.ranking = sorted(self.ranking, key=lambda x: x[1], reverse=True)
        print(self.ranking)

r = Room()