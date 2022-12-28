import src.particula as particula


class Enjambre:
    """
    Clase que modela un enjambre de partículas

    Attributes
    ----------
    poblacion: list
        Lista de partículas dentro del enjambre
    mejor_global: tuple
        Tupla con la evaluación y la posición de la mejor partícula en el enjambre durante todas las iteraciones
    fitness: function
        Función que evalúa el fitness de una partícula
    """

    def __init__(self, tam_poblacion, posicion_inicial, funcion_fitness):
        """
        Constructor de la clase Enjambre
        Parameters
        ----------
        tam_poblacion: Int
            Cantidad de partículas dentro del enjambre
        posicion_inicial: list
            Posición inicial donde inicializar las partículas
        funcion_fitness: function
            Función que evalúa el fitness de las partículas
        """
        self.poblacion = []
        self.mejor_global = None
        for i in range(tam_poblacion):
            particula_i = particula.Particula(posicion_inicial, funcion_fitness)
            if i == 0:
                self.mejor_global = particula_i
            if self.mejor_global.fitness > particula_i.fitness:
                self.mejor_global = particula_i
            self.poblacion.append(particula_i)
        self.fitness = funcion_fitness

    def optimizacion_enjambre_particulas(self, limite_superior, limite_inferior, cantidad_iteraciones):
        """
        Función que ejecuta el algoritmo de optimización por enjambre de particulas
        Parameters
        ----------
        limite_superior: list
            Limite superior del espacio de búsqueda
        limite_inferior: list
            Límite inferior del espacio de búsqueda
        cantidad_iteraciones: Int
            Iteraciones máximas que realizará el algoritmo
        Returns
        -------
        particula.Particula
            Partícula con mejor fitness
        """
        iteracion = 0
        iteracion_sin_mejora = 0
        while iteracion < cantidad_iteraciones and iteracion_sin_mejora <= 35:
            anterior_mejor_global = self.mejor_global
            for k in range(len(self.poblacion)):
                particula_k = self.poblacion[k]
                particula_k.actualiza_fitness()
                if particula_k.fitness < self.mejor_global.fitness:
                    self.mejor_global = particula_k
                    iteracion_sin_mejora = 0

            for k in range(len(self.poblacion)):
                particula_k = self.poblacion[k]
                particula_k.debo_reiniciar()
                particula_k.actualiza_velocidad(self.mejor_global.posicion)
                particula_k.actualiza_posicion(limite_superior, limite_inferior)
            if anterior_mejor_global.posicion == self.mejor_global.posicion:
                iteracion_sin_mejora += 1
            iteracion += 1
        return self.mejor_global
