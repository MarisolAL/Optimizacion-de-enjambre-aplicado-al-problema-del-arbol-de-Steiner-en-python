import numpy as np
import random


class Particula:
    """
    Clase que modela una particula dentro del enjambre.

    Attributes
    ----------
    posicion : list
        Posición donde se encuentra la partícula
    velocidad: list
        Lista con las velocidades de la particula, un elemento por cada dimension
    empeora: int
        Veces en las que una partícula empeora su fitness
    funcion_fitness: function
        Función que evalúa el fitness de una partícula
    fitness: float
        Valor del fitness de una partícula
    mejor_fitness: tuple
        Tupla con la posición y fitness donde se encontró la mejor evaluación
    """

    def __init__(self, posicion_inicial, funcion_fitness):
        """
        Parameters
        ----------
        posicion_inicial: list
            Semilla de la particula, a partir de esta posición la particula se moverá por primera vez
        funcion_fitness: function
            Función que calcula el fitness de una partícula
        """
        dimension = len(posicion_inicial)
        self.posicion = []
        self.velocidad = []
        self.empeora = 0
        self.funcion_fitness = funcion_fitness
        for i in range(dimension):
            self.velocidad.append(random.uniform(0, 1))
            self.posicion.append(posicion_inicial[i] + random.uniform(-1, 1))
        self.fitness = funcion_fitness(self.posicion)
        self.mejor_fitness = (self.fitness, self.posicion)

    def actualiza_posicion(self, limite_superior, limite_inferior):
        """
        Función que actualiza la posición de la partícula utilizando el vector de velocidades, si la posicion excede los
        límites entonces la posición es igual al límite que haya excedido
        Parameters
        ----------
        limite_superior: list
            Limite superior del espacio de búsqueda
        limite_inferior: list
            Límite inferior del espacio de búsqueda
        """
        nueva_posicion = []
        for i in range(len(self.posicion)):
            nueva_posicion.append(self.posicion[i] + self.velocidad[i])
            if nueva_posicion[i] > limite_superior[i]:
                nueva_posicion[i] = limite_superior[i]
            if nueva_posicion[i] < limite_inferior[i]:
                nueva_posicion[i] = limite_inferior[i]
        self.posicion = nueva_posicion

    def actualiza_velocidad(self, posicion_mejor_global):
        """
        Función que actualiza el vector de velocidades de una partícula
        Parameters
        ----------
        posicion_mejor_global: list
            Vector con la posicion de la mejor partícula en el enjambre
        """
        w = 0.5  # Constante de inercia
        c_1 = 1.25  # Constante cognitiva
        c_2 = 1.75  # Constante social

        r_1 = np.random.normal(0, 1, len(self.posicion))
        r_2 = np.random.normal(0, 1, len(self.posicion))

        velocidad_cognitiva = []
        velocidad_social = []

        for i in range(len(self.posicion)):
            velocidad_cognitiva.append(self.mejor_fitness[1][i] - self.posicion[i])
            velocidad_social.append(posicion_mejor_global[i] - self.posicion[i])

        nueva_velocidad = []
        for i in range(len(self.posicion)):
            momentum = w * self.velocidad[i]
            componente_cognitivo = c_1 * velocidad_cognitiva[i] * r_1[i]
            componente_social = c_2 * r_2[i] * velocidad_social[i]
            nuevo_valor = momentum + componente_social + componente_cognitivo
            nueva_velocidad.append(nuevo_valor)
        self.velocidad = nueva_velocidad

    def actualiza_fitness(self):
        """
        Función que actualiza el fitness de una partícula, ajusta si el nuevo valor es el mejor fitness y verifica si
        la particula empeoró su fitness
        """
        fitness_posicion_actual = self.fitness(self.posicion)
        self.fitness = fitness_posicion_actual
        if fitness_posicion_actual > self.mejor_fitness[0]:
            self.empeora += 1
        else:
            self.empeora = 0
            if fitness_posicion_actual < self.mejor_fitness[0]:
                self.mejor_fitness = (fitness_posicion_actual, self.posicion)

    def debo_reiniciar(self):
        """
        Función que verifica si dado el número de veces que la partícula ha empeorado su fitness, se debe reiniciar
        """
        if self.empeora >= 20:
            nueva_particula = Particula(self.posicion, self.funcion_fitness)
            self.posicion = nueva_particula.posicion
            self.velocidad = nueva_particula.velocidad
            self.empeora = 0
            self.fitness = nueva_particula.fitness
            self.mejor_fitness = nueva_particula.mejor_fitness
