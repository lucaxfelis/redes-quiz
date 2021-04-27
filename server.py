import socket
import time
import unicodedata
from threading import Thread
from quiz import *

class Server(Thread):
    
    def __init__(self,ip='localhost',port=3000):
        self.addr = (ip,port)
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.connection.bind(self.addr)
        
    def send(self, msg, porta):
        self.msg = msg.encode()
        self.connection.sendto(self.msg, ('localhost',porta))

class Room:

    def __init__(self, players_num=2):

        print("# # # # # # QUIZ RACHA-CUCA # # # # # #")
        self.players_list = []
        self.players_position = {}
        self.players_num = players_num
        
        self.server = Server()

        self.receive_players()
        self.ranking = {str(k):0 for k in self.players_list}
        self.start_game()

    def play_again(self):
        self.broadcast("QUER JOGAR NOVAMENTE? SIM OU NÃO")
        response = self.server.connection.recvfrom(1024)
        client_res = response[0].decode()
        if 's' in client_res.lower():
            self.ranking = {str(k):0 for k in self.players_list}
            self.start_game()
        else:
            self.broadcast("ATÉ LOGO!")

    def broadcast(self, msg):
        for addr in self.players_list:
            self.server.send(msg, addr)
        
    def receive_players(self):

        print("\nEsperando jogadores entrarem na sala...\n")
        while len(self.players_list) < self.players_num:
            response = self.server.connection.recvfrom(1024)
            client_res = response[0].decode()
            client_addr = response[1][1]  
            
            if client_res == 'jogar' and client_addr not in self.players_list:
                self.server.send('Entrou na sala!', client_addr)
                self.players_list.append(client_addr)

                player_pos = self.players_list.index(client_addr) + 1
                print(f'Jogador {player_pos} entrou na sala!')
                self.players_position[str(client_addr)] = player_pos
                self.server.send(f'Você é o jogador {player_pos}', client_addr)
        
        self.broadcast("Jogo começará em breve. Se prepare!")
        time.sleep(5)
        
    def start_game(self):
        print("\nA partida começou!")
        
        quiz = Quiz(questions_num = 5)
        rounds = quiz.questions_num
        
        for round in range(rounds):
            question, right_answer = quiz.get_question()
            question = f"\n# # # # PERGUNTA {round + 1} # # # #\n" + question
            print(question)
            self.broadcast(question)
            
            answer_table = {str(k):-1 for k in self.players_list}
        
            self.get_guesses(right_answer, answer_table)

        ranking = self.get_ranking()
        self.broadcast(ranking)
        print(ranking)
        self.play_again()
        
    def get_guesses(self, right_answer, answer_table):
        
        not_right = True
        #in_time = True

        while not_right:
            
            received = self.server.connection.recvfrom(1024)
            guess = self.get_unicode_str(received[0].decode())
            client_addr = received[1][1]
            if client_addr in self.players_list:
                answer_table[str(client_addr)] = 0

                if guess == self.get_unicode_str(right_answer):
                    print(f"O jogador {self.players_position[str(client_addr)]} acertou!")
                    self.server.send("Você acertou e ganhou 25 pontos!", client_addr)
                    self.ranking[str(client_addr)] += 25
                    not_right = False
                    
                else:
                    self.server.send("Você errou seu palpite e perdeu 5 pontos. Tente novamente.", client_addr)
                    self.ranking[str(client_addr)] -= 5
            else:
                self.server.send("Sala cheia, parceiro!", client_addr)
        
        for key in self.ranking.keys():
            self.ranking[key] += answer_table[key]
        
        return

    def get_ranking(self):

        self.ranking = [(k, v) for k,v in self.ranking.items()]
        self.ranking = sorted(self.ranking, key=lambda x: x[1], reverse=True)

        result = f'\n\n|{"PLACAR".center(20)}|\n'
        for player, score in self.ranking:
            result += f"|  Jogador {self.players_position[player]}  |{str(score).center(6)}|\n"
        return result

    def get_unicode_str(self, string):
        string_nova = ''.join(ch for ch in unicodedata.normalize('NFKD', string) 
        if not unicodedata.combining(ch))
        return string_nova.lower()

Room()