
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
        #linha = ",".join([str(v) for v in grafo.vertices]) + "\n"
        linha = ",".join([str(v.nivel) for v in grafo.vertices]) + "\n"
        #print(linha)
        self.fd.write(linha)


def atualizaNiveis(grafo, delta_t):
    for v in grafo.vertices:
        v.nivel += v.dejeto_medio * np.random.poisson(v.poisson_lambda * delta_t)

def simula(grafo: Graph, delta_t, duracao):
    """
    delta_t: horas
    duracao: horas
    """

    with Logging("log.txt") as log:
        for i in np.arange(0, duracao, delta_t):
            atualizaNiveis(grafo, delta_t)
            log.log_current(grafo)
            pass
        pass
