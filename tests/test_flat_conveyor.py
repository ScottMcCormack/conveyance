import os
import unittest

from conveyance import belt_capacity, conveyance, conveyor_resistances, power_requirements


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'flat_conveyor.yaml')
        self.c = conveyance.Conveyance(file_path=self.file_path)

    def test_cross_sectional_capacity(self):
        """Test the cross-sectional properties of the conveyor"""
        s = belt_capacity.belt_cs_area(l3=self.c.l3, b=self.c.b, ia=self.c.ia, sa=self.c.sa)
        self.assertAlmostEqual(s, 0.180, 3)  # s: 0.180 m^2

        q_vt = belt_capacity.volumetric_flow(belt_ca=s, v=self.c.v)
        self.assertAlmostEqual(q_vt, 0.865, 3)  # q_vt:	0.865 m^3/s

        q_mt = belt_capacity.mass_density_material(v=self.c.v, q_v=q_vt, p=self.c.p)
        self.assertAlmostEqual(q_mt, 153, 0)  # q_mt: 153 kg/m

    def test_flat_conveyor_design(self):
        """Test the design of a flat conveyor"""
        q = 2300  # (t/h)
        q_m = belt_capacity.mass_density_material(v=self.c.v, q=q)
        self.assertAlmostEqual(q_m, 133.1, 1)  # q_m: 133.1 kg/m

        # mass_density_idler_carry
        q_ro = belt_capacity.mass_density_idler(a=self.c.a_o, m=self.c.m_o)
        self.assertAlmostEqual(q_ro, 12.92, 2)  # q_ro:	12.92 kg/m

        # mass_density_idler_return
        q_ru = belt_capacity.mass_density_idler(a=self.c.a_u, m=self.c.m_u)
        self.assertAlmostEqual(q_ru, 4.40, 2)  # q_ru: 4.40 kg/m

        # Fh: Conveyor main resistance
        f_h = conveyor_resistances.resistance_main(q_m=q_m, q_b=self.c.q_b, q_ro=q_ro, q_ru=q_ru,
                                                   c_l=self.c.c_l, install_a=self.c.install_a, ff=self.c.ff)
        self.assertAlmostEqual(f_h, 5142.73, 2)  # f_h:	5142.73 N

        # Fst: Resistance due to gravity of the conveyed material
        f_st = conveyor_resistances.resistance_gravity(q_m=q_m, H=0)
        self.assertAlmostEqual(f_st, 0, 0)  # f_st: 0.0 N

        # Fba: Resistance due to inertial and frictional forces
        q_v = belt_capacity.volume_carried_material(q=q, p=self.c.p)
        f_ba = conveyor_resistances.resistance_inertial_friction(q_v=q_v, p=self.c.p, v=self.c.v, v_0=self.c.v_0)
        self.assertAlmostEqual(f_ba, 3066.7, 1)  # f_ba: 3066.7 N

        # Ff: Resistance between handled material and skirtplates in acceleration area
        f_f = conveyor_resistances.resistance_material_acceleration(q_v=q_v, p=self.c.p, v=self.c.v, v_0=self.c.v_0,
                                                                    b1=self.c.b1, mu1=self.c.mu1, mu2=self.c.mu2)
        self.assertAlmostEqual(f_f, 2390.38, 2)  # f_f: 2390.38 N

        # f_1t: Wrap resistance between the belt and the pulleys
        f_1t = conveyor_resistances.resistance_belt_wrap(B=self.c.B, wrap_a=self.c.wrap_a)
        self.assertAlmostEqual(f_1t, 360, 0)  # f_1t: 360 N

        # f_n: Calculate secondary resistances (Fn)
        f_n = conveyor_resistances.resistance_secondary(q_v=q_v, p=self.c.p, v=self.c.v, v_0=self.c.v_0,
                                                        B=self.c.B, b1=self.c.b1, mu1=self.c.mu1, mu2=self.c.mu2,
                                                        wrap_a_h=self.c.wrap_a, wrap_a_t=self.c.wrap_a)
        f_n_expected = 6177.05  # f_n: 6177.05 N
        self.assertAlmostEqual(f_n, f_n_expected, 2)
        # Sum previous components together
        self.assertAlmostEqual(f_ba + f_f + (2 * f_1t), f_n_expected, 2)

        # f_gl: Resistance due to friction between the material handled and skirt plates
        f_gl = conveyor_resistances.resistance_material_skirtplates(q_v=q_v, p=self.c.p, v=self.c.v, l_s=self.c.l_s, b1=self.c.b1, mu2=self.c.mu2)
        self.assertAlmostEqual(f_gl, 1221.34, 2)  # f_gl: 1221.34 N

        # f_rc: Friction resistance due to belt cleaners fitted to the conveyor
        f_rc = conveyor_resistances.resistance_belt_cleaners(bc_w=self.c.bc_w, bc_t=self.c.bc_t, bc_p=self.c.bc_p,
                                                             bc_n=self.c.bc_n, mu3=self.c.mu3)
        self.assertAlmostEqual(f_rc, 691.2, 1)  # f_rc: 691.2 N

        # f_s: Special resistances
        f_ep = 0
        f_a = 0
        f_s_expected = 1912.54  # f_s: 1912.54 N
        f_s = conveyor_resistances.resistance_concentrated(q_v=q_v, p=self.c.p, v=self.c.v, l_s=self.c.l_s, b1=self.c.b1,
                                                           bc_w=self.c.bc_w, bc_t=self.c.bc_t, bc_p=self.c.bc_p,
                                                           bc_n=self.c.bc_n, mu3=self.c.mu3, mu2=self.c.mu2)
        self.assertAlmostEqual(f_s, f_s_expected, 2)
        # Sum previous components together
        self.assertAlmostEqual(f_ep + f_gl + f_rc + f_a, f_s_expected, 2)

        # Determine belt sag tension force
        f_bs_min_o, f_bs_min_u = conveyor_resistances.resistance_belt_sag_tension(q_m=q_m, q_b=self.c.q_b, a_o=self.c.a_o, a_u=self.c.a_u,
                                                                                  h_a_o=self.c.h_a_o, h_a_u=self.c.h_a_u)
        self.assertAlmostEqual(f_bs_min_o, 22005, 0)  # f_bs_min_o: 22005 N
        self.assertAlmostEqual(f_bs_min_u, 3024, 0)  # f_bs_min_o: 3024 N

        # f_u: Peripheral driving force on driving pulley
        f_u = f_h + f_n + f_s + f_st
        self.assertAlmostEqual(f_u, 13232.32, 2)  # f_u: 13232.32 N

        # Calculate the drive motor power requirements
        p_m = power_requirements.power_requirements_motor(f_u=f_u, v=self.c.v, d_eta_1=self.c.d_eta_1, d_eta_2=self.c.d_eta_2)
        self.assertAlmostEqual(p_m / 1000, 68.93, 2)  # p_m: 68.93 kW

        # Check the min tensile force to transmit f_u (drive pulley)
        t_d_1, t_d_2, t_d_rat = conveyor_resistances.tension_transmit_min(f_u=f_u, wrap_a=self.c.wrap_a, mu_b=self.c.mu_b)
        self.assertAlmostEqual(t_d_1, 21680.28, 2)
        self.assertAlmostEqual(t_d_2, 8447.96, 2)
        self.assertTrue(t_d_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Check the min tensile force to avoid belt sag (tail pulley)
        t_t_1, t_t_2, t_t_rat = conveyor_resistances.tension_transmit_min(f_u=f_u, wrap_a=self.c.wrap_a, mu_b=self.c.mu_b, t_2_min=f_bs_min_o)
        self.assertAlmostEqual(t_t_1, 35237.40, 2)
        self.assertAlmostEqual(t_t_2, 22005.08, 2)
        self.assertFalse(t_t_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Calculate precise values for wrap resistance using ISO 5048
        # Drive pulley tension
        f_1t_d = conveyor_resistances.resistance_belt_wrap_iso(B=self.c.B, d=self.c.d, D=self.c.D_d, d_0=self.c.d_0_d,
                                                               m_p=self.c.m_p_d, t_1=t_t_1, t_2=t_t_2)
        self.assertAlmostEqual(f_1t_d, 153, 0)  # 153 N

        # Tail pulley tension
        f_1t_t = conveyor_resistances.resistance_belt_wrap_iso(B=self.c.B, d=self.c.d, D=self.c.D_t, d_0=self.c.d_0_t,
                                                               m_p=self.c.m_p_t, t_1=t_t_2, t_2=t_t_2)
        self.assertAlmostEqual(f_1t_t, 141, 0)  # 141 N

        # Recalculate resistances
        f_n = conveyor_resistances.resistance_secondary(q_v=q_v, p=self.c.p, v=self.c.v, v_0=self.c.v_0,
                                                        B=self.c.B, b1=self.c.b1, mu1=self.c.mu1, mu2=self.c.mu2,
                                                        wrap_a_h=self.c.wrap_a, wrap_a_t=self.c.wrap_a,
                                                        f_1t_d=f_1t_d, f_1t_t=f_1t_t)
        f_n_expected = 5751  # f_n: 5751 N
        self.assertAlmostEqual(f_n, f_n_expected, 0)
        # Sum previous components together
        self.assertAlmostEqual(f_ba + f_f + f_1t_d + f_1t_t, f_n_expected, 0)

        # f_u: Peripheral driving force on driving pulley
        f_u = f_h + f_n + f_s + f_st
        self.assertAlmostEqual(f_u, 12806, 0)  # f_u: 12806 N

        # Recalculate the drive motor power requirements
        p_m = power_requirements.power_requirements_motor(f_u=f_u, v=self.c.v, d_eta_1=self.c.d_eta_1, d_eta_2=self.c.d_eta_2)
        self.assertAlmostEqual(p_m / 1000, 66.71, 2)  # p_m: 68.93 kW
