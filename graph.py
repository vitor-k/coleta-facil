import numpy as np
import yaml


class Vertex:
    """
    Vértices do grafo, podendo ser lixeiras ou despache/depósito.
    Por simplificação há um único despache/depósito, representado por id=0.
    """
    _id = 0

    def __init__(self, id: int = None, capacidade: float = np.inf) -> None:
        if id is not None:
            self.id = id
        else:
            self.id = Vertex._id
            Vertex._id += 1
        self.capacidade = capacidade
        self.nivel = 0
        if self.id == 0:
            self.poisson_lambda = 0
            self.dejeto_medio = 0
        else:
            self.poisson_lambda = 1
            self.dejeto_medio = 0.3
        pass

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __repr__(self) -> str:
        return f"{self.id}: {self.nivel} / {self.capacidade}"

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        if self.id != 0:
            return f"{self.nivel}: {self.nivel/self.capacidade}"
        else:
            return "n/a"


class Graph:
    """
    O grafo com as distâncias mínimas entre as lixeiras.
    """

    def __init__(self, filename: str) -> None:
        with open(filename, "r") as fp:
            dados = yaml.load(fp, yaml.Loader)
            capacidades = dados["capacidades"]
            self.num_vertices = len(capacidades)
            self.vertices = list([Vertex(id=i, capacidade=c)
                                  for i, c in enumerate(capacidades)])
            if self.vertices[0].id != 0:
                self.vertices[0].id = 0

            if "pesos" in dados:
                self.matriz_adjacencia = np.array(dados["pesos"])
            else:
                self.matriz_adjacencia = None

            if "coordenadas" in dados:
                self.coordenadas = dados["coordenadas"]
            else:
                self.coordenadas = None

            if "parametros_preenchimento" in dados:
                for i in range(self.num_vertices):
                    p_lambda, dejeto = dados["parametros_preenchimento"][i]
                    self.vertices[i].poisson_lambda = p_lambda
                    self.vertices[i].dejeto_medio = dejeto
                    pass

    def distancia(self, v1: Vertex, v2: Vertex) -> float:
        """Retorna a distancia entre os vertices a partir dos ids"""
        if self.matriz_adjacencia is not None:
            return self.matriz_adjacencia[v1.id, v2.id]
        if self.coordenadas is not None:
            return np.hypot(self.coordenadas[v1.id][0] - self.coordenadas[v2.id][0], self.coordenadas[v1.id][1] - self.coordenadas[v2.id][1])

    def distancia_id(self, id1: int, id2: int) -> float:
        """Retorna a distancia entre os vertices a partir dos ids"""
        if self.matriz_adjacencia is not None:
            return self.matriz_adjacencia[id1, id2]
        if self.coordenadas is not None:
            return np.hypot(self.coordenadas[id1][0] - self.coordenadas[id2][0], self.coordenadas[id1][1] - self.coordenadas[id2][1])
