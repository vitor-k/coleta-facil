import graph
import roteamento
import random

def main():
    grafo = graph.Graph(filename="exemplo.yaml")
    for v in grafo.vertices:
        v.nivel = round(random.random() * v.capacidade)
    print(grafo.vertices)
    print(roteamento.nearestNeighbour(grafo, 100))
    pass

if __name__ == "__main__":
    main()
