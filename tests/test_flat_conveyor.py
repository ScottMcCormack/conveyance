import os
import unittest

from conveyance import belt_capacity, conveyance, conveyor_resistances, power_requirements


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'flat_conveyor.yaml')
        q = 2300  # (t/h)
        self.c = conveyance.Conveyance(file_path=self.file_path, q=q)

    def test_cross_sectional_capacity(self):
        """Test the cross-sectional properties of the conveyor"""
        self.assertAlmostEqual(self.c.s, 0.180, 3)  # s: 0.180 m^2
        self.assertAlmostEqual(self.c.q_vt, 0.865, 3)  # q_vt:	0.865 m^3/s
        self.assertAlmostEqual(self.c.q_mt, 153, 0)  # q_mt: 153 kg/m

    def test_flat_conveyor_design(self):
        """Test the design of a flat conveyor"""
        self.assertAlmostEqual(self.c.q_m, 133.1, 1)  # q_m: 133.1 kg/m

        # mass_density_idler_carry
        self.assertAlmostEqual(self.c.q_ro, 12.92, 2)  # q_ro:	12.92 kg/m

        # mass_density_idler_return
        self.assertAlmostEqual(self.c.q_ru, 4.40, 2)  # q_ru: 4.40 kg/m

        # Fh: Conveyor main resistance
        self.assertAlmostEqual(self.c.f_h, 5142.73, 2)  # f_h:	5142.73 N

        # Fst: Resistance due to gravity of the conveyed material
        self.assertAlmostEqual(self.c.f_st, 0, 0)  # f_st: 0.0 N

        # Fba: Resistance due to inertial and frictional forces
        self.assertAlmostEqual(self.c.f_ba, 3066.7, 1)  # f_ba: 3066.7 N

        # Ff: Resistance between handled material and skirtplates in acceleration area
        self.assertAlmostEqual(self.c.f_f, 2390.38, 2)  # f_f: 2390.38 N

        # f_1t: Wrap resistance between the belt and the pulleys
        self.assertAlmostEqual(self.c.f_1t, 360, 0)  # f_1t: 360 N

        # f_n: Calculate secondary resistances (Fn)
        f_n_expected = 6177.05  # f_n: 6177.05 N
        self.assertAlmostEqual(self.c.f_n, f_n_expected, 2)
        # Sum previous components together
        self.assertAlmostEqual(self.c.f_ba + self.c.f_f + (2 * self.c.f_1t), f_n_expected, 2)

        # f_gl: Resistance due to friction between the material handled and skirt plates
        self.assertAlmostEqual(self.c.f_gl, 1221.34, 2)  # f_gl: 1221.34 N

        # f_rc: Friction resistance due to belt cleaners fitted to the conveyor
        self.assertAlmostEqual(self.c.f_rc, 691.2, 1)  # f_rc: 691.2 N

        # f_s: Special resistances
        f_ep = 0
        f_a = 0
        f_s_expected = 1912.54  # f_s: 1912.54 N
        self.assertAlmostEqual(self.c.f_s, f_s_expected, 2)
        # Sum previous components together
        self.assertAlmostEqual(f_ep + self.c.f_gl + self.c.f_rc + f_a, f_s_expected, 2)

        # Determine belt sag tension force
        self.assertAlmostEqual(self.c.f_bs_min_o, 22005, 0)  # f_bs_min_o: 22005 N
        self.assertAlmostEqual(self.c.f_bs_min_u, 3024, 0)  # f_bs_min_o: 3024 N

        # f_u: Peripheral driving force on driving pulley
        self.assertAlmostEqual(self.c.f_u, 13232.32, 2)  # f_u: 13232.32 N

        # Calculate the drive motor power requirements
        self.assertAlmostEqual(self.c.p_m / 1000, 68.93, 2)  # p_m: 68.93 kW

        # Recalculate using the ISO method
        self.c.calculate_iso_method()

        # Check the min tensile force to transmit f_u (drive pulley)
        self.assertAlmostEqual(self.c.t_d_1, 21680.28, 2)
        self.assertAlmostEqual(self.c.t_d_2, 8447.96, 2)
        self.assertTrue(self.c.t_d_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Check the min tensile force to avoid belt sag (tail pulley)
        self.assertAlmostEqual(self.c.t_t_1, 35237.40, 2)
        self.assertAlmostEqual(self.c.t_t_2, 22005.08, 2)
        self.assertFalse(self.c.t_t_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Calculate precise values for wrap resistance using ISO 5048
        self.assertAlmostEqual(self.c.f_1t_d, 153, 0)  # 153 N

        # Tail pulley tension
        self.assertAlmostEqual(self.c.f_1t_t, 141, 0)  # 141 N

        # Recalculate resistances
        f_n_expected = 5751  # f_n: 5751 N
        self.assertAlmostEqual(self.c.f_n, f_n_expected, 0)
        # Sum previous components together
        self.assertAlmostEqual(self.c.f_ba + self.c.f_f + self.c.f_1t_d + self.c.f_1t_t, f_n_expected, 0)

        # f_u: Peripheral driving force on driving pulley
        self.assertAlmostEqual(self.c.f_u, 12806, 0)  # f_u: 12806 N

        # Recalculate the drive motor power requirements
        self.assertAlmostEqual(self.c.p_m / 1000, 66.71, 2)  # p_m: 66.71 kW
