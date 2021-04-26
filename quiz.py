import random

class Quiz:
    """Representa o quiz a ser jogado."""

    def __init__(self, questions_num=5, file_path="tuples.txt"):
        """
        Inicia o quiz gerando sua lista de questões e respostas
        de um tamanho pré-determinado.
        
        Parâmetros:
            questions_num: número de questões (deafult 5) 
            file_path: caminho do arquivo auxiliar (default tuples.txt)
        """

        # recebe o número de questões do quiz
        self.questions_num = int(questions_num)

        questions_list = self.get_questions_list()
        # lista final de questões
        self.questions = questions_list[0]
        # lista final de respostas
        self.answers = questions_list[1]

    def selectSequence(self):
        """ Retorna a sequencia das perguntas."""
        return [random.randrange(0,2) for x in range(0,self.questions_num)]

    def selectQuestion (self):
        """Retorna a lista com as tuplas de perguntas e respostas."""

        # abre o arquivo e pega as linhas
        self.arq = open('tuples.txt', 'r')
        self.allask = self.arq.readlines()
        self.arq.close()

        # vetores para armaenzar os indíces e perguntas
        self.indicador = []
        self.perguntas = []

        # faz o sorteio aleatório do numeros de quais perguntas serão selecionadas
        while len(self.indicador) != self.questions_num:
            self.number = random.randrange(0,27)
            if self.number not in self.indicador:
                self.indicador.append(self.number)

        #adiciona as perguntas em relaçãos aos números 
        for x in self.indicador:
            self.perguntas.append(self.allask[x])

        # transformas as strings em tuplas
        for i in range(0, self.questions_num):
            self.broken=self.perguntas[i].split(',')
            self.a = self.broken[0][2:-1]
            self.b = self.broken[1][2:-3]
            self.junto = (self.a,self.b)
            self.perguntas.append(self.junto)

        #retira as strings
        for x in range(0, self.questions_num):
            self.perguntas.pop(0)

        #retorna a lista com as tuplas de respostas
        return self.perguntas

    def get_questions_list(self):
        """
        Retorna tupla com lista de questões e lista de respostas
        definitivas.
        """
        self.respostas = self.selectQuestion()
        self.sequencia = self.selectSequence()
        self.gabarito =[]
        self.questionario =[]

        for x in range(0,self.questions_num):
            if self.sequencia[x] == 0:
                self.pergunta = f'Qual a capital do estado {self.respostas[x][0]}: ______________ ?'
                self.questionario.append(self.pergunta)
                self.gabarito.append(self.respostas[x][1])
            else:
                self.pergunta = f'Qual a estado tem a capital {self.respostas[x][1]}: ______________ ?'
                self.questionario.append(self.pergunta)
                self.gabarito.append(self.respostas[x][0])

        return (self.questionario,self.gabarito)

    def get_question(self):
        """
        Retorna uma tupla com uma questão e sua respectiva
        reposta retirando da lista de questões e respostas.
        """
        
        return self.questions.pop(), self.answers.pop()
