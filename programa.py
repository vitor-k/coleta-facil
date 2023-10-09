import graph
import roteamento
import random
import argparse


def main(filepath):
    grafo = graph.Graph(filename=filepath)
    for v in grafo.vertices:
        v.nivel = round(max(0.7, random.random()) * v.capacidade)
    print(grafo.vertices)
    nos_relevantes = set([v.id for v in grafo.vertices
                          if (v.id != 0) and 
                          (v.nivel / v.capacidade > 0.6)])

    print("Nos relevantes: ", list([grafo.vertices[i] for i in nos_relevantes]))
    
    print("k-medoids:", roteamento.kMedoidsClustering(grafo, nos_relevantes, 100))

    print("Uma rota do nearest neighbour: ",
          roteamento.nearestNeighbour(grafo, nos_relevantes, 100))

    print("As rotas pelo savings: ", roteamento.savingsAlgorithm(
        grafo, nos_relevantes, 100))
    
    print("As rotas pelo cluster first, route second: ", roteamento.clusterFirstRouteSecond(
        grafo, nos_relevantes, 100))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Coleta Facil",
        description="Realiza o roteamento a partir de heurísticas")
    parser.add_argument("filepath", nargs='?', default="exemplo.yaml")
    args = parser.parse_args()
    main(args.filepath)
