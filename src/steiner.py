import math
import networkx as nx
import src.enjambre as enjambre
from src.util import distancia_entre_dos_puntos, calcula_peso_total_grafica
import random


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

    def borra_steiner(self):
        """
        Función que elimina los datos del objeto Steiner
        """
        self.puntos = []
        self.peso = 0
        self.arbol = None

    def calcula_arbol_euclidiano_minimo(self):
        """
        Función que calcula dado el conjunto de puntos inicial el arbol generador de peso
        mínimo euclidiano.
        """
        grafica = nx.Graph()
        for punto_i in self.puntos:
            grafica.add_node(tuple(punto_i))
        for punto_i in self.puntos:
            for punto_j in self.puntos:
                if (not punto_i == punto_j) \
                        and (not grafica.has_edge(tuple(punto_i),
                                                  tuple(punto_j))):
                    peso = distancia_entre_dos_puntos(punto_i, punto_j)
                    grafica.add_edge(tuple(punto_i),
                                     tuple(punto_j),
                                     weight=peso)
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

    def obten_limite_superior(self):
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

    def fitness_problema_steiner(self, nuevo_punto):
        """
        Función que calcula el fitness de un nuevo punto dentro de una gráfica
        preexistente
        Parameters
        ----------
        nuevo_punto: tuple
            Punto que se agregará a la gráfica preexistente
        Returns
        -------
        float
            Valor del peso del nuevo arbol
        """
        nuevo_arbol = self.calcula_arbol_con_punto(nuevo_punto)
        peso_nuevo_arbol = calcula_peso_total_grafica(nuevo_arbol)
        return peso_nuevo_arbol

    def optimizacion_particulas_steiner(self, iteracion_max, cantidad_enjambres, tam_poblacion, no_max_puntos=math.inf):
        """
        Función que ejecuta el algoritmo de optimización por enjambre de partículas sobre el problema del
        arbol de Steiner
        Parameters
        ----------
        iteracion_max: int
            Iteraciones máximas deseadas para cada enjambre
        cantidad_enjambres: int
            Cantidad de enjambres que se crearán para ejecutarlos de uno en uno
        tam_poblacion: int
            Tamaño de población para los enjambres, todos los enjambres tendrán el mismo tamaño
        no_max_puntos: int
            Número máximo de puntos Steiner a encontrar
        Returns
        -------
        list
            Lista con los puntos originales y los puntos steiner y el peso final obtenido agregando los puntos
        """
        print("Peso original ", str(self.peso))
        lim_min = self.obten_limite_inferior()
        lim_max = self.obten_limite_superior()
        nuevos_puntos_steiner = []
        enjambre_actual = 0
        while enjambre_actual < cantidad_enjambres and len(nuevos_puntos_steiner) < no_max_puntos:
            abscisa_inicial = random.uniform(lim_min[0], lim_max[0])
            ordenada_inicial = random.uniform(lim_min[1], lim_max[1])
            posicion_inicial = [abscisa_inicial, ordenada_inicial]
            enjambre_i = enjambre.Enjambre(tam_poblacion, posicion_inicial, self.fitness_problema_steiner)
            mejor_particula = enjambre_i.optimizacion_enjambre_particulas(lim_min,
                                                                          lim_max,
                                                                          iteracion_max)
            nuevo_punto_steiner = mejor_particula.posicion
            nuevo_fitness_steiner = mejor_particula.fitness
            if nuevo_fitness_steiner < self.peso:
                nuevos_puntos_steiner.append(nuevo_punto_steiner)
                self.puntos.append(nuevo_punto_steiner)
                self.calcula_arbol_euclidiano_minimo()
                self.calcula_peso_total_arbol()
            enjambre_actual += 1
        print("Peso final ", self.peso, " con los puntos ", self.puntos)
        return [self.puntos, self.peso, nuevos_puntos_steiner]
