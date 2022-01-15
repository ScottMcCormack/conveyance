import unittest

from conveyance import belt_capacity


class TestBeltCapacity(unittest.TestCase):
    def setUp(self):
        # Vars for mass_density_material
        self.v = 4.8  # Belt speed (m/s)
        self.p = 0.85  # Density, coal (t/m^3)
        self.q_v = 0.864  # (m^3/s)
        self.q = 2300  # (t/h)

        # Vars for mass_density_idler
        self.a_o = 1.2
        self.m_o = 15.5
        self.a_u = 3.0
        self.m_u = 13.2

    def test_mass_density_throughput(self):
        q_m = belt_capacity.mass_density_material(v=self.v, q=self.q)
        self.assertAlmostEqual(q_m, 133.1, 1)

    def test_mass_density_flow_rate(self):
        q_m = belt_capacity.mass_density_material(v=self.v, q_v=self.q_v, p=self.p)
        self.assertAlmostEqual(q_m, 153, 0)

    def test_mass_density_idler_carry(self):
        q_ro = belt_capacity.mass_density_idler(a=self.a_o, m=self.m_o)
        self.assertAlmostEqual(q_ro, 12.92, 2)

    def test_mass_density_idler_return(self):
        q_ro = belt_capacity.mass_density_idler(a=self.a_u, m=self.m_u)
        self.assertAlmostEqual(q_ro, 4.40, 2)
