import src.steiner as steiner
import unittest


class SteinerTest(unittest.TestCase):
    def test_constructor_steiner(self):
        s = steiner.Steiner([(0,0), (0,1), (2,0)])
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


if __name__ == '__main__':
    unittest.main()
