import math


def distancia_entre_dos_puntos(punto_1, punto_2):
    """Función que calcula la distancia entre dos puntos con dimensión n."""
    distancia = 0
    for i in range(0, len(punto_1)):
        distancia += pow((punto_2[i] - punto_1[i]), 2)
    return math.sqrt(distancia)

a = [1, 1, 1]
b = [1, 0, 1]
print(distancia_entre_dos_puntos(a, b))