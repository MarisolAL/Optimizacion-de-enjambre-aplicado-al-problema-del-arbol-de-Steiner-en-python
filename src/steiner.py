import networkx as nx
import src.enjambre as enjambre
from src.util import distancia_entre_dos_puntos

class Steiner:

    def __init__(self, puntos):
        self.puntos = puntos
        self.arbol = self.obten_arbol
        self.peso = self.obten_peso_total(self.arbol)

    def obten_arbol(self):
        grafica = nx.Graph()
        for punto_i in self.puntos:
            grafica.add_node(punto_i)
        for punto_i in self.puntos:
            for punto_j in self.puntos:
                if (not punto_i == punto_j) and (not grafica.has_edge(punto_i, punto_j)):
                    grafica.add_edge(punto_i, punto_j, weight=distancia_entre_dos_puntos(punto_i, punto_j))
        arbol = nx.minimum_spanning_tree(grafica)
        for arista_i in arbol.edges:
            peso = distancia_entre_dos_puntos(arista_i[0], arista_i[1])
            arbol.add_edge(arista_i[0], arista_i[1], weight=peso)
        return arbol

