import numpy as np
from scipy.signal import convolve2d as conv2
from queue import PriorityQueue

class Estado:
    def __init__(self, pai=None, matriz=None):
        self.pai = pai
        self.matriz = matriz
        self.d = 0  # tamanho do caminho inicio - estado
        self.c = 0
        self.p = 0  # prioridade

    def __eq__(self, other):
        return np.array_equal(self.matriz, other.matriz)

    def __lt__(self, other):
        return self.p < other.p

    def __hash__(self):
        return hash(tuple(self.matriz.flatten())) # O hash deixa a matriz, como um vetor, deixando, portanto, unidimensional, facilitando a análise posterior

    def mostrar(self):
        for i in self.matriz:
            print(i)
        print()

def acoes_permitidas(estado):
    adj = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    blank = estado.matriz == 9
    mask = conv2(blank, adj, 'same')
    return estado.matriz[np.where(mask)]

def movimentar(s, c):
    matriz = s.matriz.copy()
    matriz[np.where(s.matriz == 9)] = c
    matriz[np.where(s.matriz == c)] = 9
    return Estado(matriz=matriz)

def dist(t1, t2):
    return np.sum(list(map(lambda i, j: abs(i - j), t1, t2)))

def manhattan(estado):
    obj = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    return np.sum([dist(np.where(obj == i), np.where(estado.matriz == i)) for i in range(1, 9)])

def hamming(s):
    obj = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    qtde_fora_lugar = len(s.matriz[np.where(s.matriz != obj)])
    return (qtde_fora_lugar - 1 if qtde_fora_lugar > 0 else 0)

def solucao(estado):
    flat = estado.matriz.flatten()
    flat = flat[flat != 9]  # Remove o espaço vazio (9)
    inversoes = 0

    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversoes += 1

    return inversoes % 2 == 0

def solubilidade(s, f, o):
    if not solucao(s):
        print("Não tem solução")
        return

    retorno = astar(s, f, o)
    if retorno != o:
        print("Não tem solução")
    else:
        print("O jogo tem solução")

def astar(s, f, o):
    Q = PriorityQueue()
    vetor = set()
    caminho_percorrido = 0

    s.p = 0
    Q.put((s.p, s))

    while not Q.empty():
        v = Q.get()[1]
        caminho_percorrido += 1

        if v == o:
            print(f"Caminhos percorridos: {caminho_percorrido}")
            # print(f"Custo até o estado objetivo: {v.d}")
            return v

        vetor.add(v) #É adicionado ao vetor o estado já passado, do qual não será revisitado, portanto, faz a remoção dos estados repetitivos

        for a in acoes_permitidas(v):
            u = movimentar(v, a)

            if u not in vetor:
                u.d = v.d + 1
                u.pai = v
                u.p = f(u) + u.d
                vetor.add(u)
                Q.put((u.p, u))
                u.mostrar()

    print(f"Caminhos percorridos: {caminho_percorrido}")
    # print(f"Custo até o estado objetivo: {v.d}")
    return s

o = Estado(matriz=np.array([[1, 2, 3], [4, 5, 6],[7, 8, 9]]))


# s = Estado(matriz=np.array([[4, 1 , 3], [ 9, 2, 5],[7, 8, 6]]))
#s = Estado(matriz=np.array([[9 , 1, 3], [4, 2, 5],[7, 8, 6]]))
#s = Estado(matriz=np.array([[4, 9, 5], [3, 8 ,6],[7, 1, 2]]))
#s = Estado(matriz=np.array([[4, 6, 7], [9, 5, 8],[2, 1, 3]]))
# s = Estado(matriz=np.array([[5, 3, 2], [7, 6, 4],[8, 1, 9]]))
s = Estado(matriz=np.array([[1, 2, 3], [4, 6, 5], [8, 7, 9]])) 
# s = Estado(matriz=np.array([[1, 2, 3], [4, 5, 6], [8, 7, 9]])) #nao tem solucao

# solubilidade(s, hamming, o)
solubilidade(s, manhattan, o)