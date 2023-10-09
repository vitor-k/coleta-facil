import unittest

import graph
import roteamento
import random


class TesteRoteamento(unittest.TestCase):

    def testa_rotas_validas_savings(self):
        grafo = graph.Graph(filename="exemplo.yaml")
        for v in grafo.vertices:
            v.nivel = round(random.random() * v.capacidade)
        nos_relevantes = set([v.id for v in grafo.vertices
                              if (v.id != 0) and (v.nivel / v.capacidade > 0.6)])

        for capacidade in [60, 80, 100, 120]:
            rotas = roteamento.savingsAlgorithm(grafo, nos_relevantes,
                                                capacidade)
            for rota in rotas:
                total = sum([x.nivel for x in rota])
                self.assertGreaterEqual(capacidade, total)

    def testa_rotas_validas_clustering(self):
        grafo = graph.Graph(filename="exemplo.yaml")
        for v in grafo.vertices:
            v.nivel = round(random.random() * v.capacidade)
        nos_relevantes = set([v.id for v in grafo.vertices
                              if (v.id != 0) and (v.nivel / v.capacidade > 0.6)])

        for capacidade in [60, 80, 100, 120]:
            rotas = roteamento.clusterFirstRouteSecond(grafo, nos_relevantes,
                                                       capacidade)
            for rota in rotas:
                total = sum([x.nivel for x in rota])
                self.assertGreaterEqual(capacidade, total)


if __name__ == '__main__':
    unittest.main()
