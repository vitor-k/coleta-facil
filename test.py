import unittest

import graph
import roteamento
import random


class TesteRoteamento(unittest.TestCase):

    def testa_rotas_validas(self):
        grafo = graph.Graph(filename="exemplo.yaml")
        for v in grafo.vertices:
            v.nivel = round(random.random() * v.capacidade)
        nos_relevantes = [(v.id != 0) and
                          (v.nivel/v.capacidade > 0.6)
                          for v in grafo.vertices]

        for capacidade in [60, 80, 100, 120]:
            rotas = roteamento.savingsAlgorithm(grafo, nos_relevantes,
                                                capacidade)
            for rota in rotas:
                total = sum([x.nivel for x in rota])
                self.assertGreaterEqual(capacidade, total)


if __name__ == '__main__':
    unittest.main()
