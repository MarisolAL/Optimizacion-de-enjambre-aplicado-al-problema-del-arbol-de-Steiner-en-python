import src.enjambre as enjambre
import src.particula as particula
import unittest


class EnjambreTest(unittest.TestCase):
    def test_constructor_enjambre(self):
        e = enjambre.Enjambre(5, [0, 0], sum)
        self.assertEqual(len(e.poblacion), 5, 'La cantidad de particulas debe ser igual que las ingresadas')
        for p in e.poblacion:
            self.assertIsInstance(p, particula.Particula, 'Todos los individuos deben ser partículas')
        self.assertEqual(e.fitness, sum, 'La función fitness debe igual a la ingresada')


if __name__ == '__main__':
    unittest.main()
