
import random
from math import ceil
from graph import *
import numpy as np
import itertools


def custoVerticeCluster(grafo: Graph, cluster: set[int], v: int) -> float:
    total = 0
    for e in cluster - set([v]):
        total += grafo.distancia_id(v, e)
    return total


def custoCluster(grafo: Graph, cluster: set[int]) -> float:
    total = 0
    for v in cluster:
        total += custoVerticeCluster(grafo, cluster, v)
    return total


def custoRota(grafo: Graph, rota: list[Vertex]) -> float:
    """
    Calcula o custo total de uma rota
    """
    total = 0
    total += grafo.distancia_id(0, rota[0].id)
    for i in range(len(rota)-1):
        total += grafo.distancia(rota[i], rota[i+1])
    total += grafo.distancia_id(rota[-1].id, 0)
    return total


def kMedoidsClustering(grafo: Graph, nos_relevantes: set[int],
                       capacidade: int) -> list[set[int]]:
    """
    Realiza a clusterização por k medoids por otimização alternada
    """
    vertices = [v for v in range(grafo.num_vertices) if v in nos_relevantes]

    # Estima o valor de k a partir da capacidade e dos niveis
    niveis = [grafo.vertices[v].nivel for v in vertices]
    nivel_total = sum(niveis)

    k = ceil(nivel_total / capacidade) or 1

    clusters_excessivos = True
    while clusters_excessivos:
        clusters_excessivos = False
        medoids = random.sample(vertices, k)

        continuar = True
        custo_novo = np.inf
        while continuar:
            custo_anterior = custo_novo
            continuar = False
            clusters = list([set([m]) for m in medoids])
            for v in vertices:
                cluster = medoids.index(
                    min(medoids, key=lambda x: grafo.distancia_id(v, x)))
                clusters[cluster] |= set([v])
                pass

            for i in range(len(clusters)):
                cluster = clusters[i]
                medoids[i] = min(cluster, key=lambda x: custoVerticeCluster(grafo, cluster, x))
            custo_novo = sum([custoCluster(grafo, cluster)
                            for cluster in clusters])
            if custo_novo < custo_anterior:
                continuar = True
        for cluster in clusters:
            total = sum([grafo.vertices[x].nivel for x in cluster])
            if total > capacidade:
                clusters_excessivos = True
        if clusters_excessivos:
            k += 1

    return clusters


def nearestNeighbour(grafo: object, nos_relevantes: set[int]):
    """
    Implementa um algoritmo greedy para resolver o Problema do Caixeiro Viajante.
    """
    rota = []
    parada = False
    no_atual = 0
    while not parada:
        mais_proximo = None
        menor_distancia = np.inf
        for i in range(grafo.num_vertices):
            if i not in nos_relevantes:
                continue
            if grafo.vertices[i] not in rota \
                    and grafo.distancia_id(no_atual, i) < menor_distancia:
                mais_proximo = i
                menor_distancia = grafo.distancia_id(no_atual, i)
        if mais_proximo is None:
            parada = True
        else:
            rota.append(grafo.vertices[mais_proximo])
            no_atual = mais_proximo
    return rota


def buscaPCV(grafo: object, nos_relevantes: set[int]):
    """
    Implementa um algoritmo de busca exaustiva para resolver o Problema do Caixeiro Viajante.
    """
    vertices = [v for v in grafo.vertices if v.id in nos_relevantes]
    rotas = itertools.permutations(vertices)
    return list(min(rotas, key= lambda x: custoRota(grafo, x)))


def clusterFirstRouteSecond(grafo: object, nos_relevantes: set[int],
                            capacidade: int, forca_bruta = None) -> list[Vertex]:
    """
    Implementa uma heurística para o Problema de Roteamento de Veículos
    baseado na formação de clusters em que se resolve o Problema do 
    Caixeiro Viajante
    """
    clusters = kMedoidsClustering(grafo, nos_relevantes, capacidade)
    rotas = []
    for cluster in clusters:
        if forca_bruta is True or (forca_bruta is None and len(cluster) < 10):
            rotas.append(buscaPCV(grafo, nos_relevantes & cluster))
        else:
            rotas.append(nearestNeighbour(grafo, nos_relevantes & cluster))


    return rotas


def savingsAlgorithm(grafo: object, nos_relevantes: set[int],
                     capacidade_veiculo: int) -> list[Vertex]:
    """
    Implementa a heurística para o Problema de Roteamento de Veículos
    conhecida como algoritmo de savings ou algoritmo de Clarke e Wright.
    """
    rotas = []

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
                savings[(i, j)] = grafo.distancia_id(0, primeira_rota_fim) \
                    + grafo.distancia_id(segunda_rota_inicio, 0) \
                    - grafo.distancia_id(primeira_rota_fim, segunda_rota_inicio)

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
