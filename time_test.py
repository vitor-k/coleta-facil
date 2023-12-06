
import graph
import roteamento

import random

import timeit

setup = """
import graph
import roteamento
import random

dados = {}
dados["coordenadas"] = [(x//10, x%10) for x in range(10*10)]
dados["capacidades"] = 10*10*[100]
grafo = graph.Graph(dados=dados)
for v in grafo.vertices:
    v.nivel = 14
"""

for i in range(5,25,2):
    print(min(timeit.Timer(f'a=set(random.sample(range(10*10), {i})); roteamento.savingsAlgorithm(grafo, a, 100)', setup=setup).repeat(7, 100)), end=';')
    print(min(timeit.Timer(f'a=set(random.sample(range(10*10), {i})); roteamento.clusterFirstRouteSecond(grafo, a, 100, True)', setup=setup).repeat(7, 100)), end=';')
    print(min(timeit.Timer(f'a=set(random.sample(range(10*10), {i})); roteamento.clusterFirstRouteSecond(grafo, a, 100, False)', setup=setup).repeat(7, 100)))

