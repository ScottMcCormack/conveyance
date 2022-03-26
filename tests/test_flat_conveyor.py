import unittest

from conveyance import belt_capacity, conveyor_resistances, cross_section


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        # Assume 3-roll configuration using coal
        self.l3 = 0.436  # Width of the idler (3 roll set)
        self.B = 1.2  # Total width of the belt (m)
        self.b = 1.03  # Width of max material on belt (m)
        self.ia = 45  # Idlers angle (deg)
        self.sa = 20  # Material surcharge angle, coal (deg)
        self.b1 = 0.75  # Width between skirtplates (m)

        # Vars for mass_density_material
        self.v = 4.8  # Belt speed (m/s)
        self.v_0 = 0  # Speed of conveyed material (m/s)
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
        self.c_l = 143  # Center-to-centre length of the conveyor (m)
        self.install_a = 0  # Installation angle of the conveyor (deg)
        self.wrap_a = 90  # Wrap angle around the pulley (deg)
        self.ff = 0.02  # Artificial friction factor (average operating conditions)
        self.mu1 = 0.5  # Coefficients between material/belt
        self.mu2 = 0.7  # Coefficients between material/skirtplates

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

        # Fh: Conveyor main resistance
        f_h = conveyor_resistances.resistance_main(q_m=q_m, q_b=self.q_b, q_ro=q_ro, q_ru=q_ru,
                                                   c_l=self.c_l, install_a=self.install_a, ff=self.ff)
        self.assertAlmostEqual(f_h, 5142.73, 2)  # f_h:	5142.73 N

        # Fst: Resistance due to gravity of the conveyed material
        f_st = conveyor_resistances.resistance_gravity(q_m=q_m, H=0)
        self.assertAlmostEqual(f_st, 0, 0)  # f_st: 0.0 N

        # Fba: Resistance due to inertial and frictional forces
        q_v = belt_capacity.volume_carried_material(q=q, p=self.p)
        f_ba = conveyor_resistances.resistance_inertial_friction(q_v=q_v, p=self.p, v=self.v, v_0=self.v_0)
        self.assertAlmostEqual(f_ba, 3066.7, 1)  # f_ba: 3066.7 N

        # Ff: Resistance between handled material and skirtplates in acceleration area
        f_f = conveyor_resistances.resistance_material_acceleration(q_v=q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                                    b1=self.b1, mu1=self.mu1, mu2=self.mu2)
        self.assertAlmostEqual(f_f, 2390.38, 2)  # f_f: 2390.38 N

        # f_1t: Wrap resistance between the belt and the pulleys
        f_1t = conveyor_resistances.resistance_belt_wrap(B=self.B, wrap_a=self.wrap_a)
        self.assertAlmostEqual(f_1t, 360, 0)  # f_1t: 360 N

        # f_n: Calculate secondary resistances (Fn)
        f_n = conveyor_resistances.resistance_secondary(q_v=q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                        B=self.B, b1=self.b1, mu1=self.mu1, mu2=self.mu2,
                                                        wrap_a_h=self.wrap_a, wrap_a_t=self.wrap_a)
        f_n_expected = 6177.05  # f_n: 6177.05 N
        self.assertAlmostEqual(f_n, f_n_expected, 2)
        self.assertAlmostEqual(f_ba + f_f + (2 * f_1t), f_n_expected, 2)  # Sum previous components together
