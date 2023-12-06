
from graph import *
from roteamento import *
import numpy as np


class Logging:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self):
        self.fd = open(self.filename, "w")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fd.close()

    def log_current(self, grafo: Graph):
        linha = ",".join([str(v.nivel) for v in grafo.vertices]) + "\n"
        self.fd.write(linha)


class Trabalhador:
    def __init__(self, grafo, rota) -> None:
        self.grafo = grafo
        self.rota = rota
        self.velocidade = 3.6 * 50000  # 1m/s * 50 px/m
        self.progresso = 0
        self.indice_rota = 0
        self.custos = [grafo.distancia_id(0, rota[0].id)] + [grafo.distancia(rota[i], rota[i + 1]) for i in range(len(rota) - 1)] + [grafo.distancia_id(rota[-1].id, 0)]
        self.acabou = False

    def avanca(self, delta_t):
        if self.acabou:
            return
        self.progresso += self.velocidade * delta_t
        while self.progresso >= self.custos[self.indice_rota]:
            self.progresso -= self.custos[self.indice_rota]

            self.grafo.vertices[0].nivel += self.rota[self.indice_rota].nivel
            self.rota[self.indice_rota].nivel = 0

            self.indice_rota += 1

            if self.indice_rota >= len(self.rota):
                self.acabou = True
                return


def simula(grafo: Graph, delta_t, duracao):
    """
    delta_t: horas
    duracao: horas
    """

    with Logging("log.csv") as log:
        trabalhadores = []
        for i in np.arange(0, duracao, delta_t):
            grafo.atualizaNiveis(delta_t)
            log.log_current(grafo)

            nos_relevantes = set([v.id for v in grafo.vertices
                                  if (v.id != 0) and (v.nivel / v.capacidade > 0.6)])
            if len(nos_relevantes) > 3 and len(trabalhadores) == 0:
                rotas = savingsAlgorithm(grafo, nos_relevantes, 100)
                trabalhadores = [Trabalhador(grafo, rota) for rota in rotas]
                print(trabalhadores)
            for trabalhador in trabalhadores:
                trabalhador.avanca(delta_t)
            trabalhadores = list([x for x in trabalhadores if x.acabou is False])

        pass
