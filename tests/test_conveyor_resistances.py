import unittest

from conveyance import conveyor_resistances


class TestBeltCapacity(unittest.TestCase):
    def setUp(self):
        self.q_m = 133.1
        self.q_b = 16.44
        self.q_ro = 12.92
        self.q_ru = 4.40
        self.c_l = 143
        self.install_a = 0
        self.ff = 0.02

    def test_mass_density_throughput(self):
        q_m = conveyor_resistances.resistance_main(q_m=self.q_m, q_b=self.q_b, q_ro=self.q_ro, q_ru=self.q_ru,
                                                   c_l=self.c_l, install_a=self.install_a, ff=self.ff)
        self.assertAlmostEqual(q_m, 5142.73, 1)
