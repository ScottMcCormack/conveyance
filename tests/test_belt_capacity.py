import unittest

from conveyance import belt_capacity


class TestBeltCapacity(unittest.TestCase):
    def setUp(self):
        self.v = 4.8  # Belt speed (m/s)
        self.p = 0.85  # Density, coal (t/m^3)
        self.q_v = 0.864  # (m^3/s)
        self.q = 2300  # (t/h)

    def test_mass_density_throughput(self):
        q_m = belt_capacity.mass_density_material(v=self.v, q=self.q)
        self.assertAlmostEqual(q_m, 133.1, 1)

    def test_mass_density_flow_rate(self):
        q_m = belt_capacity.mass_density_material(v=self.v, q_v=self.q_v, p=self.p)
        self.assertAlmostEqual(q_m, 153, 0)
