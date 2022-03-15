import unittest

from conveyance import belt_capacity, conveyor_resistances, cross_section


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        # Assume 3-roll configuration using coal
        self.l3 = 0.436
        self.b = 1.03
        self.ia = 45
        self.sa = 20
        self.v = 4.8  # Belt speed (m/s)

        # Vars for mass_density_material
        self.p = 0.85  # Density, coal (t/m^3)
        self.q_v = 0.864  # (m^3/s)
        self.q = 2300  # (t/h)

        # Vars for mass_density_idler
        self.a_o = 1.2
        self.m_o = 15.5
        self.a_u = 3.0
        self.m_u = 13.2

        # Vars for conveyor resistances
        self.q_b = 16.44
        self.c_l = 143
        self.install_a = 0
        self.ff = 0.02

    def test_mass_density_flow_rate(self):
        q_mt = belt_capacity.mass_density_material(v=self.v, q_v=self.q_v, p=self.p)
        self.assertAlmostEqual(q_mt, 153, 0)

    # cross_section
    def test_cross_section(self):
        # Cross-sectional area of material on the belt
        s = cross_section.belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s, 0.180, 3)

        # Flow rate of the conveyor
        q_vt = cross_section.belt_capacity(belt_ca=s, v=self.v)
        self.assertAlmostEqual(q_vt, 0.865, 3)

    def test_conveyor_resistance(self):
        q_m = belt_capacity.mass_density_material(v=self.v, q=self.q)
        self.assertAlmostEqual(q_m, 133.1, 1)

        # mass_density_idler_carry
        q_ro = belt_capacity.mass_density_idler(a=self.a_o, m=self.m_o)
        self.assertAlmostEqual(q_ro, 12.92, 2)

        # mass_density_idler_return
        q_ru = belt_capacity.mass_density_idler(a=self.a_u, m=self.m_u)
        self.assertAlmostEqual(q_ru, 4.40, 2)

        # Conveyor main resistance
        q_m = conveyor_resistances.resistance_main(q_m=q_m, q_b=self.q_b, q_ro=q_ro, q_ru=q_ru,
                                                   c_l=self.c_l, install_a=self.install_a, ff=self.ff)
        self.assertAlmostEqual(q_m, 5142.73, 1)
