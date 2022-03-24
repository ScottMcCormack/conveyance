import unittest

from conveyance import belt_capacity, conveyor_resistances, cross_section


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        # Assume 3-roll configuration using coal
        self.l3 = 0.436  # Width of the idler (3 roll set)
        self.b = 1.03  # Width of max material on belt
        self.ia = 45  # Idlers angle
        self.sa = 20  # Material surcharge angle, coal

        # Vars for mass_density_material
        self.v = 4.8  # Belt speed (m/s)
        self.p = 0.85  # Density, coal (t/m^3)
        self.q_v = 0.864  # (m^3/s)
        self.q = 2300  # (t/h)

        # Vars for mass_density_idler
        self.a_o = 1.2  # Carry idler spacing (m)
        self.m_o = 15.5  # Carry idler mass (kg)
        self.a_u = 3.0  # Return idler spacing (m)
        self.m_u = 13.2  # Return idler mass (kg)

        # Vars for conveyor resistances
        self.q_b = 16.44  # Belt mass (kg/m)
        self.c_l = 143  # Center-to-centre length of the conveyor
        self.install_a = 0  # Installation angle of the conveyor (deg)
        self.ff = 0.02  # Artificial friction factor (average operating conditions)

    def test_cross_sectional_capacity(self):
        """Test the cross-sectional properties of the conveyor"""
        s = cross_section.belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s, 0.180, 3)  # s: 0.180 m^2

        q_vt = cross_section.belt_capacity(belt_ca=s, v=self.v)
        self.assertAlmostEqual(q_vt, 0.865, 3)  # q_vt:	0.865 m^3/s

        q_mt = belt_capacity.mass_density_material(v=self.v, q_v=q_vt, p=self.p)
        self.assertAlmostEqual(q_mt, 153, 0)  # q_mt: 153 kg/m

    def test_flat_conveyor_design(self):
        """Test the design of a flat conveyor"""
        q = 2300  # (t/h)
        q_m = belt_capacity.mass_density_material(v=self.v, q=q)
        self.assertAlmostEqual(q_m, 133.1, 1)  # q_m: 133.1 kg/m

        # mass_density_idler_carry
        q_ro = belt_capacity.mass_density_idler(a=self.a_o, m=self.m_o)
        self.assertAlmostEqual(q_ro, 12.92, 2)  # q_ro:	12.92 kg/m

        # mass_density_idler_return
        q_ru = belt_capacity.mass_density_idler(a=self.a_u, m=self.m_u)
        self.assertAlmostEqual(q_ru, 4.40, 2)  # q_ru: 4.40 kg/m

        # Conveyor main resistance
        f_m = conveyor_resistances.resistance_main(q_m=q_m, q_b=self.q_b, q_ro=q_ro, q_ru=q_ru,
                                                   c_l=self.c_l, install_a=self.install_a, ff=self.ff)
        self.assertAlmostEqual(f_m, 5142.73, 2)  # f_h:	5142.73 N
