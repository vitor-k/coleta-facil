
import random
from math import ceil
from graph import *
import numpy as np


def custoVerticeCluster(grafo: Graph, cluster: set[int], v: int):
    total = 0
    for e in cluster-set([v]):
        total += grafo.distancia_id(v,e)
    return total


def custoCluster(grafo: Graph, cluster: set[int]):
    total = 0
    for v in cluster:
        total += custoVerticeCluster(grafo, cluster, v)
    return total


def kMedoidsClustering(grafo: Graph, nos_relevantes: set[int], capacidade: int) -> list[set[int]]:
    vertices = [v for v in range(grafo.num_vertices) if v in nos_relevantes]

    # Estima o valor de k a partir da capacidade e dos niveis
    niveis = [grafo.vertices[v].nivel for v in vertices]
    nivel_total = sum(niveis)

    k = ceil(nivel_total/capacidade)

    medoids = random.sample(vertices, k)

    continuar = True
    custo_novo = np.inf
    while continuar:
        custo_anterior = custo_novo
        continuar = False
        clusters = list([set([m]) for m in medoids])
        for v in vertices:
            cluster = medoids.index(min(medoids, key=lambda x: grafo.distancia_id(v,x)))
            clusters[cluster] |= set([v])
            pass

        for i in range(len(clusters)):
            cluster = clusters[i]
            medoids[i] = min(cluster, key=lambda x:custoVerticeCluster(grafo, cluster, x))
        custo_novo = sum([custoCluster(grafo, cluster) for cluster in clusters])
        if custo_novo < custo_anterior:
            continuar = True

    return clusters


def nearestNeighbour(grafo: object, nos_relevantes: set[int],
                     capacidade: int):
    rota = []
    parada = False
    no_atual = 0
    nivel_previsto = 0
    while not parada:
        distancias = grafo.matriz_adjacencia[no_atual, :]
        mais_proximo = None
        menor_distancia = np.inf
        for i in range(len(distancias)):
            if i not in nos_relevantes:
                continue
            if grafo.vertices[i] not in rota \
                    and distancias[i] < menor_distancia:
                mais_proximo = i
                menor_distancia = distancias[i]
        if mais_proximo is None:
            parada = True
        elif nivel_previsto + grafo.vertices[mais_proximo].nivel < capacidade:
            rota.append(grafo.vertices[mais_proximo])
            nivel_previsto += grafo.vertices[mais_proximo].nivel
            no_atual = mais_proximo
        else:
            parada = True
    return rota


def clusterFirstRouteSecond(grafo: object, nos_relevantes: set[int],
                     capacidade: int):
    clusters = kMedoidsClustering(grafo, nos_relevantes, capacidade)
    rotas = []
    for cluster in clusters:
        rotas.append(nearestNeighbour(grafo, nos_relevantes & cluster, capacidade))
    
    return rotas

def savingsAlgorithm(grafo: object, nos_relevantes: set[int],
                     capacidade_veiculo: int):
    rotas = []
    distancia = grafo.matriz_adjacencia

    # faz as rotas iniciais
    for i in range(1, grafo.num_vertices):
        if i not in nos_relevantes:
            continue
        # implicito que inicia em 0 e finaliza em 0
        rotas.append([i])

    savings_possiveis = True
    while savings_possiveis:
        savings = {}
        savings_possiveis = False
        for i in range(len(rotas)):
            for j in range(len(rotas)):
                if i == j:
                    continue
                # verificar se a rota e possivel
                nivel_previsto = sum(
                    [grafo.vertices[v].nivel for v in rotas[i] + rotas[j]])
                if nivel_previsto >= capacidade_veiculo:
                    continue

                primeira_rota_fim = rotas[i][-1]
                segunda_rota_inicio = rotas[j][0]
                savings[(i, j)] = distancia[0, primeira_rota_fim] \
                    + distancia[segunda_rota_inicio, 0] \
                    - distancia[primeira_rota_fim, segunda_rota_inicio]

        if not savings:
            break
        maximo_savings = max(savings, key=savings.get)
        if savings[maximo_savings] > 0:
            savings_possiveis = True
            (i, j) = maximo_savings
            nova_rota = rotas[i] + rotas[j]
            for indice in sorted([i, j], reverse=True):
                rotas.pop(indice)
            rotas.append(nova_rota)
        pass
    rotas_finais = []
    for rota in rotas:
        rotas_finais.append(list([grafo.vertices[x] for x in rota]))
    return rotas_finais
