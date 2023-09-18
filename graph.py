import numpy as np
import yaml


class Vertex:
    """
    Vértices do grafo, podendo ser lixeiras ou despache/depósito.
    Por simplificação há um único despache/depósito, representado por id=0.
    """
    _id = 0

    def __init__(self, id: int = None, capacidade: float = 0) -> None:
        if id is not None:
            self.id = id
        else:
            self.id = Vertex._id
            Vertex._id += 1
        self.capacidade = capacidade
        self.nivel = 0
        pass

    def __eq__(self, __o: object) -> bool:
        return self.id == __o.id

    def __repr__(self) -> str:
        return f"{self.id}: {self.nivel} / {self.capacidade}"

    def __str__(self) -> str:
        if self.id != 0:
            return f"Lixeira {self.id}: Nível={self.nivel}, Capacidade={self.capacidade}"
        else:
            return "Depósito"


class Graph:
    """
    O grafo com as distâncias mínimas entre as lixeiras.
    """

    def __init__(self, num_vertices: int = 0, filename: str = None) -> None:
        if filename is not None:
            with open(filename, "r") as fp:
                dados = yaml.load(fp, yaml.Loader)
                print(dados)
                capacidades = dados["capacidades"]
                self.num_vertices = len(capacidades)
                self.vertices = list([Vertex(capacidade=c) for c in capacidades])
                if self.vertices[0].id != 0:
                    self.vertices[0].id = 0
                self.matriz_adjacencia = np.array(dados["pesos"])
                print(self.matriz_adjacencia)
            return
            pass

        self.vertices = num_vertices*[None]
        self.i_preenchido = 0

        self.matriz_adjacencia = np.ndarray((num_vertices, num_vertices))

        pass

    def insereVertice(self, vertice: Vertex) -> None:
        """Insere o vertice se houver espaço.

        Args:
            vertice: o vertice a ser inserido.

        Returns:
            None
        """
        if self.vertices[self.i_preenchido] is None:
            self.vertices[self.i_preenchido] = vertice
            self.i_preenchido += 1
        pass

    def populaMatriz(self, distancias: dict):
        pass

