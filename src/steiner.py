import networkx as nx
import src.enjambre as enjambre
from src.util import distancia_entre_dos_puntos

class Steiner:
    """
    Clase que modela el problema del árbol de Steiner

    Attributes
    ----------
    puntos: list
        Puntos pertenecientes al conjunto inicial del problema
    arbol: list
        Lista de aristas pertenecientes al árbol euclideano de peso mínimo
    peso: float
        Número con el valor del peso del árbol
    """

    def __init__(self, puntos):
        self.puntos = puntos
        self.arbol = None
        self.peso = None

    def calcula_arbol_euclidiano_minimo(self):
        """
        Función que calcula dado el conjunto de puntos inicial el arbol generador de peso
        mínimo euclidiano y lo regresa.
        :return: list
            Regresa la lista de aristas que forman el árbol de peso mínimo euclidiano
        """
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

    def obten_peso_total_arbol(self):
        """
        Función que calcula el peso total del árbol en el conjunto de puntos.
        :return: float
            Suma de los pesos de las aristas del árbol
        """
        peso_total = 0
        print(self.arbol)
        for arista in self.arbol.edges.data('weight', default=1000):
            print(arista)
            peso_total += arista[2]
        return peso_total

steiner = Steiner([(-8,5),(10,2),(50,-20),(1,24)])
print(steiner.arbol)
arbol = steiner.calcula_arbol_euclidiano_minimo()
print(arbol)
