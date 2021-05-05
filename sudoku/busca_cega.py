from queue import Queue
import copy
import time

class Sudoku(object):
    def __init__(self, initial):
        self.initial = initial
        self.tamanho = len(initial)
        self.altura = int(self.tamanho/3)

    def filtrar_valores(self, valores, usado):
        return [valor for valor in valores if valor not in usado]

    def acha_quadro(self, board, estado):
        for linha in range(board):
            for coluna in range(board):
                if estado[linha][coluna] == 0:
                    return linha, coluna   

    def acoes(self, estado):
        numeros = range(1, self.tamanho + 1)
        em_coluna = []
        em_quadrante = []

        linha,coluna = self.acha_quadro(self.tamanho, estado)

        # Filtra valores em linha
        usados = [valor for valor in estado[linha] if (valor != 0)]
        opcoes = self.filtrar_valores(numeros, usados)

        # Filtra valores em colunas
        for index_coluna in range(self.tamanho):
            if estado[index_coluna][coluna] != 0:
                em_coluna.append(estado[index_coluna][coluna])
        opcoes = self.filtrar_valores(opcoes, em_coluna)

        # Filtra valores em quadrante
        inicio_linha = int(linha / self.altura) * self.altura
        inicio_coluna = int(coluna / 3) * 3
        
        for bloco_linha in range(0, self.altura):
            for bloco_coluna in range(0, 3):
                em_quadrante.append(estado[inicio_linha + bloco_linha][inicio_coluna + bloco_coluna])
        opcoes = self.filtrar_valores(opcoes, em_quadrante)

        for numero in opcoes:
            yield numero, linha, coluna      

    # Retorna o board apos uma atualizacao
    def resultado(self, estado, acao):
        novo_estado = copy.deepcopy(estado)
        novo_estado[acao[1]][acao[2]] = acao[0]

        return novo_estado

    # Soma linhas, colunas e quadrantes pra saber se board esta valido
    def verifica_validade(self, estado):
        total = sum(range(1, self.tamanho + 1))

        # Verifica linhas e colunas
        for linha in range(self.tamanho):
            if (len(estado[linha]) != self.tamanho) or (sum(estado[linha]) != total):
                return False

            total_coluna = 0
            for coluna in range(self.tamanho):
                total_coluna += estado[coluna][linha]

            if (total_coluna != total):
                return False

        # Verifica quadrante
        for coluna in range(0, self.tamanho, 3):
            for linha in range(0, self.tamanho, self.altura):

                total_quadrante = 0
                for linha_quadrante in range(0, self.altura):
                    for coluna_quadrante in range(0, 3):
                        total_quadrante += estado[linha + linha_quadrante][coluna + coluna_quadrante]

                if (total_quadrante != total):
                    return False

        return True

class Nodo:
    def __init__(self, estado, acao = None):
        self.estado = estado
        self.acao = acao

    # Usa acoes para criar um novo estado do Sudoku
    def expand(self, sudoku):
        return [self.nodo_filho(sudoku, acao)
                for acao in sudoku.acoes(self.estado)]

    # Retorna nodo com novo estado
    def nodo_filho(self, sudoku, acao):
        proximo = sudoku.resultado(self.estado, acao)
        return Nodo(proximo, acao)

def BFS(sudoku):
    # Cria nodo inicial do Sudoku contendo board original
    node = Nodo(sudoku.initial)
    
    if sudoku.verifica_validade(node.estado):
        return node

    fronteira = Queue()
    fronteira.put(node)

    while (fronteira.qsize() != 0):
        node = fronteira.get()
        for filho in node.expand(sudoku):
            if sudoku.verifica_validade(filho.estado):
                return filho

            fronteira.put(filho)

    return None

def bfs_resultado(board):
    print("Resolvendo com busca em largura...")
    inicio = time.time()

    sudoku = Sudoku(board)
    solucao = BFS(sudoku)
    demora = time.time() - inicio

    if solucao:
        print ("Solucao encontrada")
        file = open("busca-cega.txt", "w")
        for index_linha, linha in enumerate(solucao.estado):
            if(index_linha == 3 or index_linha == 6):
                file.write("------+-------+------\n")
            
            str_linha = "".join([str(valor) for valor in linha])
            file.write(" ".join([char for char in "|".join([str_linha[i:i+3] for i in range(0, len(str_linha), 3)])]) + "\n")
        file.close
    else:
        print ("Nao foi possivel resolver")

    print ("Desafio resolvido em " + str(demora) + " segundos")