
from graph import *
import numpy as np

def nearestNeighbour(grafo: object, capacidade_veiculo: int):
    rota = []
    parada = False
    no_atual = 0
    nivel_previsto = 0
    while not parada:
        distancias = grafo.matriz_adjacencia[no_atual,:]
        mais_proximo = None
        menor_distancia = np.inf
        for i in range(len(distancias)):
            if grafo.vertices[i] not in rota and distancias[i] < menor_distancia:
                mais_proximo = i
                menor_distancia = distancias[i]
        if mais_proximo is None:
            parada = True
        elif nivel_previsto + grafo.vertices[mais_proximo].nivel < capacidade_veiculo:
            rota.append(grafo.vertices[mais_proximo])
            nivel_previsto += grafo.vertices[mais_proximo].nivel
            no_atual = mais_proximo
        else:
            parada = True
    pass
    return rota
