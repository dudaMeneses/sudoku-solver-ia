import copy
import time

class Sudoku(object):
    def __init__(self, initial):
        self.initial = initial
        self.tamanho = len(initial) 
        self.altura = int(self.tamanho / 3)

    def verifica_validade(self, estado):
        maximo = sum(range(1, self.tamanho + 1))

        # Verifica linha e coluna
        for linha in range(self.tamanho):
            if (len(estado[linha]) != self.tamanho) or (sum(estado[linha]) != maximo):
                return False
            soma_coluna = 0
            for coluna in range(self.tamanho):
                soma_coluna += estado[coluna][linha]
            if (soma_coluna != maximo):
                return False

        # Verifica quadrante
        for coluna in range(0, self.tamanho, 3):
            for linha in range(0, self.tamanho, self.altura):
                soma_quadrante = 0
                for linha_quadrante in range(0, self.altura):
                    for coluna_quadrante in range(0,3):
                        soma_quadrante += estado[linha + linha_quadrante][coluna + coluna_quadrante]

                if (soma_quadrante != maximo):
                    return False
        return True

    # Retorna valores validos nao usados
    def filtra_valores(self, valores, usados):
        return [valor for valor in valores if valor not in usados]

    # Retorna quadro vazio com menor numero de opcoes
    def acha_quadro(self, board, estado):
        opcao_alvo = board
        linha = 0
        while linha < board:
            coluna = 0
            while coluna < board:
                if estado[linha][coluna] == 0:
                    opcoes = self.filtra_linha(estado, linha)
                    opcoes = self.filtra_coluna(opcoes, estado, coluna)
                    opcoes = self.filtra_quadrante(opcoes, estado, linha, coluna)
                    if len(opcoes) < opcao_alvo:
                        opcao_alvo = len(opcoes)
                        opcoes = []
                        linha_alvo = linha
                        coluna_alvo = coluna
                coluna = coluna + 1
            linha = linha + 1                
        return linha_alvo, coluna_alvo

    # Filtra valores baseados na linha
    def filtra_linha(self, estado, linha):
        valores = range(1, self.tamanho + 1) # Define valores que podem ser atribuidos ao board
        usados = [valor for valor in estado[linha] if (valor != 0)]
        opcoes = self.filtra_valores(valores, usados)
        return opcoes

    # Filtra valores baseados na coluna
    def filtra_coluna(self, opcoes, estado, coluna):
        usados = []
        for coluna_index in range(self.tamanho):
            if estado[coluna_index][coluna] != 0:
                usados.append(estado[coluna_index][coluna])
        opcoes = self.filtra_valores(opcoes, usados)
        return opcoes

    # Filtra valores baseado no quadrante
    def filtra_quadrante(self, opcoes, estado, linha, coluna):
        no_quadrante = []
        linha_inicio = int(linha/self.altura) * self.altura
        coluna_inicio = int(coluna/3) * 3
        
        for linha_quadrante in range(0, self.altura):
            for coluna_quadrante in range(0,3):
                no_quadrante.append(estado[linha_inicio + linha_quadrante][coluna_inicio + coluna_quadrante])
        opcoes = self.filtra_valores(opcoes, no_quadrante)
        return opcoes    

    def acoes(self, estado):
        linha,coluna = self.acha_quadro(self.tamanho, estado) # Acha o primeiro quadro vazio no board

        # Remove opcoes invalidas
        opcoes = self.filtra_linha(estado, linha)
        opcoes = self.filtra_coluna(opcoes, estado, coluna)
        opcoes = self.filtra_quadrante(opcoes, estado, linha, coluna)

        # Retorna uma opcao para cada estado valido
        for valor in opcoes:
            new_estado = copy.deepcopy(estado)
            new_estado[linha][coluna] = valor
            yield new_estado

class Nodo:
    def __init__(self, estado):
        self.estado = estado

    def expandir(self, sudoku):
        # Retorna lista de estados validos
        return [Nodo(estado) for estado in sudoku.acoes(self.estado)]

def DFS(sudoku):
    inicio = Nodo(sudoku.initial)
    if sudoku.verifica_validade(inicio.estado):
        return inicio.estado

    pilha = []
    pilha.append(inicio) # Adiciona estado inicial na pilha

    while pilha: 
        node = pilha.pop() # Remove ultimo nodo da pilha, testa nodo e expando as opcoes a partir deste
        if sudoku.verifica_validade(node.estado):
            return node.estado
        pilha.extend(node.expandir(sudoku)) 

    return None

def h_resultado(board):
    print ("Resolvendo com busca em profundidade e heuristicas...")

    inicio = time.time()
    sudoku = Sudoku(board)
    solucao = DFS(sudoku)
    duracao = time.time() - inicio

    if solucao:
        print ("Solucao encontrada")
        file = open("busca-heuristica.txt", "w")
        for index_linha, linha in enumerate(solucao):
            if(index_linha == 3 or index_linha == 6):
                file.write("------+-------+------\n")
            
            str_linha = "".join([str(valor) for valor in linha])
            file.write(" ".join([char for char in "|".join([str_linha[i:i+3] for i in range(0, len(str_linha), 3)])]) + "\n")
        file.close
    else:
        print ("Nao foi possivel resolver")

    print ("Duracao: " + str(duracao) + " segundos")