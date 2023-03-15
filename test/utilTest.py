import unittest
import networkx as nx

import src.util as util


class UtilTest(unittest.TestCase):
    def test_distancia_dos_puntos_caso_base(self):
        punto_1 = [0, 0]
        punto_2 = [0, 0]
        self.assertEqual(util.distancia_entre_dos_puntos(punto_1, punto_2),
                         0,
                         "Debe ser 0")

    def test_distancia_dos_puntos(self):
        punto_1 = [1, 1, 1]
        punto_2 = [0, 1, 1]
        self.assertEqual(util.distancia_entre_dos_puntos(punto_1, punto_2), 1, "Debe ser 1")

    def test_calcula_peso_total_grafica(self):
        grafica = nx.Graph()
        grafica.add_node((0, 1))
        grafica.add_node((0, 0))
        peso_arista = util.distancia_entre_dos_puntos((0, 1), (0, 0))
        grafica.add_edge((0, 1), (0, 0),
                         weight=peso_arista)
        peso = util.calcula_peso_total_grafica(grafica)
        self.assertEqual(peso, 1, 'El peso debe ser igual a 1')


if __name__ == '__main__':
    unittest.main()
