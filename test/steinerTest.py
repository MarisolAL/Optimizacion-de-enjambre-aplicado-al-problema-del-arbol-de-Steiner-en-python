import src.steiner as steiner
import unittest
from src.util import calcula_peso_total_grafica


class SteinerTest(unittest.TestCase):
    def test_constructor_steiner(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        self.assertEqual(len(s.puntos), 3)
        self.assertEqual(s.arbol, None)
        self.assertEqual(s.peso, None)

    def test_calcula_arbol(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calcula_arbol_euclidiano_minimo()
        self.assertEqual(len(s.arbol.edges), 2)

    def test_peso_total(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calcula_arbol_euclidiano_minimo()
        s.calcula_peso_total_arbol()
        self.assertEqual(s.peso, 3)

    def test_calcula_arbol_con_punto(self):
        s = steiner.Steiner([(0, 0), (0, 1), (2, 0)])
        s.calcula_arbol_euclidiano_minimo()
        nuevo_arbol = s.calcula_arbol_con_punto((1, 1))
        self.assertEqual(len(nuevo_arbol.edges), 3, 'La cantidad de aristas debe ser 3')
        peso_nuevo_arbol = calcula_peso_total_grafica(nuevo_arbol)
        self.assertLessEqual(peso_nuevo_arbol, 3.5, 'El peso del nuevo arbol debe ser menor a 3.5')

    def test_limite_superior(self):
        s = steiner.Steiner([(-9, 8), (-7, 3), (-2, 7), (9, 9),
                             (10, -8), (-10, 9), (4, 0)])
        limite_superior = s.obten_limite_superior()
        self.assertEqual(limite_superior, [10, 9])

    def test_limite_inferior(self):
        s = steiner.Steiner([(-9, 8), (-7, 3), (-2, 7), (9, 9),
                             (10, -8), (-10, 9), (4, 0)])
        limite_inferior = s.obten_limite_inferior()
        self.assertEqual(limite_inferior, [-10, -8])

    def test_optimizacion_steiner(self):
        s = steiner.Steiner([(-4, 0), (0, 6), (4, 0)])
        s.calcula_arbol_euclidiano_minimo()
        s.calcula_peso_total_arbol()
        puntos_steiner = s.optimizacion_particulas_steiner(30, 10, 15)
        self.assertGreaterEqual(len(puntos_steiner[0]), len(s.puntos))
        self.assertLessEqual(puntos_steiner[1], s.peso)


if __name__ == '__main__':
    unittest.main()
