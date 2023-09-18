import graph
import roteamento
import random


def main():
    grafo = graph.Graph(filename="exemplo.yaml")
    for v in grafo.vertices:
        v.nivel = round(random.random() * v.capacidade)
    print(grafo.vertices)
    nos_relevantes = [(v.id != 0) and (v.nivel/v.capacidade > 0.6) for v in grafo.vertices]

    print("Nos relevantes: ", list([grafo.vertices[i] for i in range(len(nos_relevantes)) if nos_relevantes[i]]))

    print("Uma rota do nearest neighbour: ", roteamento.nearestNeighbour(grafo, nos_relevantes, 100))

    print("As rotas pelo savings: ", roteamento.savingsAlgorithm(grafo, nos_relevantes, 100))
    pass


if __name__ == "__main__":
    main()
