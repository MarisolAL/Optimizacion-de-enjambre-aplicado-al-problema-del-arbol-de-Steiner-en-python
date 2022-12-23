import networkx as nx
import src.enjambre as enjambre
from src.util import distancia_entre_dos_puntos, calcula_peso_total_grafica


class Steiner:
    """
    Clase que modela el problema del árbol de Steiner

    Attributes
    ----------
    puntos: list
        Puntos pertenecientes al conjunto inicial del problema
    arbol: nx. Graph
        Lista de aristas pertenecientes al árbol euclideano de peso mínimo
    peso: float
        Número con el valor del peso del árbol
    """

    def __init__(self, puntos):
        """
        Constructor de la clase steiner
        Parameters
        ----------
        puntos: list
            Puntos que pertenecientes al conjunto inicial del problema
        """
        self.puntos = puntos
        self.arbol = None
        self.peso = None

    def calcula_arbol_euclidiano_minimo(self):
        """
        Función que calcula dado el conjunto de puntos inicial el arbol generador de peso
        mínimo euclidiano y lo regresa.
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
        self.arbol = arbol

    def calcula_peso_total_arbol(self):
        """
        Función que calcula el peso total del árbol en el conjunto de puntos y la asigna
        al atributo `peso`.
        """
        self.peso = calcula_peso_total_grafica(self.arbol)

    def calcula_arbol_con_punto(self, punto):
        """
        Función que dado un punto calcula el árbol generador de peso mínimo euclideano del conjunto
        inicial de puntos y el punto recibido
        Parameters
        ----------
        punto: tuple
            Punto agregado al conjunto inicial de puntos para calcular el árbol.
        Returns
        -------
        nx.Graph
            El arbol generador de peso mínimo incluyendo al punto pasado como parámetro
        """
        nuevos_puntos = self.puntos + [punto]
        nuevo_steiner = Steiner(nuevos_puntos)
        nuevo_steiner.calcula_arbol_euclidiano_minimo()
        return nuevo_steiner.arbol

    def obten_limite_superior(self):  # TODO: Hacer pruebas
        """
        Función que calcula las coordenadas máximas del conjunto de puntos
        Returns
        -------
        list
            Lista con el valor de la abscisa máxima y la ordenada máxima
        """
        abscisa_max = self.puntos[0][0]
        ordenada_max = self.puntos[0][1]
        for punto in self.puntos:
            if punto[0] > abscisa_max:
                abscisa_max = punto[0]
            if punto[1] > ordenada_max:
                ordenada_max = punto[1]
        return [abscisa_max, ordenada_max]

    def obten_limite_inferior(self):
        """
        Función que calcula las coordenadas mínimas del conjunto de puntos
        Returns
        -------
        list
            Lista con el valor de la abscisa mínima y la ordenada mínima
        """
        abscisa_min = self.puntos[0][0]
        ordenada_min = self.puntos[0][1]
        for punto in self.puntos:
            if punto[0] < abscisa_min:
                abscisa_min = punto[0]
            if punto[1] < ordenada_min:
                ordenada_min = punto[1]
        return [abscisa_min, ordenada_min]
