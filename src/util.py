import math
import networkx as nx

def distancia_entre_dos_puntos(punto_1, punto_2):
    """Función que calcula la distancia entre dos puntos con dimensión n."""
    distancia = 0
    for i in range(0, len(punto_1)):
        distancia += pow((punto_2[i] - punto_1[i]), 2)
    return math.sqrt(distancia)


def calcula_peso_total_grafica(grafica):
    """
    Función que calcula el peso total de una gráfica con aristas
    Parameters
    ----------
    grafica: nx.Graph
        Gráfica a la cual se le obtendrá el peso de sus aristas
    Returns
    -------
    float
        Peso de la suma de las aristas de la gráfica
    """
    peso_total = 0
    for arista in grafica.edges.data('weight', default=1000):
        peso_total += arista[2]
    return peso_total
