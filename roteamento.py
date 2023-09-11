
from graph import *
import numpy as np

def nearestNeighbour(grafo: object, nos_relevantes: list, capacidade_veiculo: int):
    rota = []
    parada = False
    no_atual = 0
    nivel_previsto = 0
    while not parada:
        distancias = grafo.matriz_adjacencia[no_atual,:]
        mais_proximo = None
        menor_distancia = np.inf
        for i in range(len(distancias)):
            if not nos_relevantes[i]:
                continue
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
    return rota

def savingsAlgorithm(grafo: object, nos_relevantes: list, capacidade_veiculo: int):
    rotas = []
    distancia = grafo.matriz_adjacencia

    # faz as rotas iniciais
    for i in range(1,grafo.num_vertices):
        if not nos_relevantes[i]:
            continue
        # implicito que inicia em 0 e finaliza em 0
        rotas.append([i])

    savings_possiveis = True
    while savings_possiveis:
        savings = {}
        savings_possiveis = False
        for i in range(len(rotas)):
            for j in range(len(rotas)):
                if i==j:
                    continue
                # verificar se a rota e possivel
                nivel_previsto = sum([grafo.vertices[v].nivel for v in rotas[i]+rotas[j]])
                if nivel_previsto >= capacidade_veiculo:
                    continue

                primeira_rota_fim = rotas[i][-1]
                segunda_rota_inicio = rotas[j][0]
                savings[(i,j)] = distancia[0,primeira_rota_fim] + distancia[segunda_rota_inicio,0] - distancia[primeira_rota_fim,segunda_rota_inicio]

        if not savings:
            break
        maximo_savings = max(savings,key=savings.get)
        if savings[maximo_savings] > 0:
            savings_possiveis = True
            (i, j) = maximo_savings
            nova_rota = rotas[i] + rotas[j]
            for indice in sorted([i,j], reverse=True):
                rotas.pop(indice)
            rotas.append(nova_rota)
        pass
    rotas_finais = []
    for rota in rotas:
        rotas_finais.append(list([grafo.vertices[x] for x in rota]))
    return rotas_finais
