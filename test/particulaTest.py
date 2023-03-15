import src.particula as particula
import unittest


class ParticulaTest(unittest.TestCase):
    def test_constructor_particula(self):
        p = particula.Particula([1, 1], sum)
        for v in p.velocidad:
            self.assertLessEqual(v, 1, 'La velocidad en cada posición se encuentra entre 0 y 1')
            self.assertGreaterEqual(v, 0, 'La velocidad en cada posición se encuentra entre 0 y 1')
        self.assertEqual(p.posicion, p.mejor_fitness[1], 'En la primera iteración la posición actual es la '
                                                         'posición con mejor fitness')
        self.assertEqual(p.empeora, 0, 'En la primera iteración la particula no ha empeorado su fitness')
        self.assertLessEqual(p.mejor_fitness[0], 4, 'El primer fitness a lo más es 4')


if __name__ == '__main__':
    unittest.main()
