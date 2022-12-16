import unittest
import src.util as util


class UtilTest(unittest.TestCase):
    def test_distancia_dos_puntos_caso_base(self):
        punto_1 = [0, 0]
        punto_2 = [0, 0]
        self.assertEqual(util.distancia_entre_dos_puntos(punto_1, punto_2), 0, "Debe ser 0")

    def test_distancia_dos_puntos(self):
        punto_1 = [1, 1, 1]
        punto_2 = [0, 1, 1]
        self.assertEqual(util.distancia_entre_dos_puntos(punto_1, punto_2), 1, "Debe ser 1")


if __name__ == '__main__':
    unittest.main()
