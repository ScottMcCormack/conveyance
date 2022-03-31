import unittest

from conveyance import belt_capacity, conveyor_resistances, power_requirements


class TestFlatConveyor(unittest.TestCase):
    def setUp(self):
        # Assume 3-roll configuration using coal
        self.l3 = 0.436  # Width of the idler (3 roll set)
        self.B = 1.2  # Total width of the belt (m)
        self.d = 0.0125  # Thickness of the belt (m)
        self.b = 1.03  # Width of max material on belt (m)
        self.ia = 45  # Idlers angle (deg)
        self.sa = 20  # Material surcharge angle, coal (deg)
        self.b1 = 0.75  # Width between skirtplates (m)
        self.l_s = 4.8  # Length of installation fitted with skirtplates (m)

        # Vars for mass_density_material
        self.v = 4.8  # Belt speed (m/s)
        self.v_0 = 0  # Speed of conveyed material (m/s)
        self.p = 0.85  # Density, coal (t/m^3)
        self.q_v = 0.864  # (m^3/s)
        self.q = 2300  # (t/h)

        # Vars for idlers
        self.a_o = 1.2  # Carry idler spacing (m)
        self.m_o = 15.5  # Carry idler mass (kg)
        self.h_a_o = 0.01  # Allowable belt sag, carry side (m)
        self.a_u = 3.0  # Return idler spacing (m)
        self.m_u = 13.2  # Return idler mass (kg)
        self.h_a_u = 0.02  # Allowable belt sag, return side (m)

        # Vars for conveyor resistances
        self.q_b = 16.44  # Belt mass (kg/m)
        self.c_l = 143  # Center-to-centre length of the conveyor (m)
        self.install_a = 0  # Installation angle of the conveyor (deg)
        self.wrap_a = 180  # Wrap angle around the pulley (deg)
        self.ff = 0.02  # Artificial friction factor (average operating conditions)
        self.mu1 = 0.5  # Coefficients between material/belt
        self.mu2 = 0.7  # Coefficients between material/skirtplates

        # Vars for belt cleaners
        self.bc_w = 1.2  # Belt cleaner width (m)
        self.bc_t = 8 / 1000  # Belt cleaner thickness (m)
        self.bc_p = 3 * 10 ** 4  # Pressure between cleaner and belt
        self.bc_n = 4  # Number of belt cleaners (three at head end, one at tail end)
        self.mu3 = 0.6  # Friction coefficient between belt and cleaner

        # Vars for drive pulley
        self.d_eta_1 = 0.95  # Fluid coupling efficiency
        self.d_eta_2 = 0.97  # Gearbox efficiency
        self.mu_b = 0.3  # Belt/Pulley friction coefficient
        self.d_0_d = 0.14  # Diameter of inside bearing
        self.D_d = 0.6  # Drive pulley diameter
        self.m_p_d = 1050  # Drive pulley mass

        # Vars for tail pulley
        self.d_0_t = 0.12  # Diameter of inside bearing
        self.D_t = 0.5  # Tail pulley diameter
        self.m_p_t = 800  # Tail pulley mass

    def test_cross_sectional_capacity(self):
        """Test the cross-sectional properties of the conveyor"""
        s = belt_capacity.belt_cs_area(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s, 0.180, 3)  # s: 0.180 m^2

        q_vt = belt_capacity.volumetric_flow(belt_ca=s, v=self.v)
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
        # Sum previous components together
        self.assertAlmostEqual(f_ba + f_f + (2 * f_1t), f_n_expected, 2)

        # f_gl: Resistance due to friction between the material handled and skirt plates
        f_gl = conveyor_resistances.resistance_material_skirtplates(q_v=q_v, p=self.p, v=self.v, l_s=self.l_s, b1=self.b1, mu2=self.mu2)
        self.assertAlmostEqual(f_gl, 1221.34, 2)  # f_gl: 1221.34 N

        # f_rc: Friction resistance due to belt cleaners fitted to the conveyor
        f_rc = conveyor_resistances.resistance_belt_cleaners(bc_w=self.bc_w, bc_t=self.bc_t, bc_p=self.bc_p,
                                                             bc_n=self.bc_n, mu3=self.mu3)
        self.assertAlmostEqual(f_rc, 691.2, 1)  # f_rc: 691.2 N

        # f_s: Special resistances
        f_ep = 0
        f_a = 0
        f_s_expected = 1912.54  # f_s: 1912.54 N
        f_s = conveyor_resistances.resistance_concentrated(q_v=q_v, p=self.p, v=self.v, l_s=self.l_s, b1=self.b1,
                                                           bc_w=self.bc_w, bc_t=self.bc_t, bc_p=self.bc_p,
                                                           bc_n=self.bc_n, mu3=self.mu3, mu2=self.mu2)
        self.assertAlmostEqual(f_s, f_s_expected, 2)
        # Sum previous components together
        self.assertAlmostEqual(f_ep + f_gl + f_rc + f_a, f_s_expected, 2)

        # Determine belt sag tension force
        f_bs_min_o, f_bs_min_u = conveyor_resistances.resistance_belt_sag_tension(q_m=q_m, q_b=self.q_b, a_o=self.a_o, a_u=self.a_u,
                                                                                  h_a_o=self.h_a_o, h_a_u=self.h_a_u)
        self.assertAlmostEqual(f_bs_min_o, 22005, 0)  # f_bs_min_o: 22005 N
        self.assertAlmostEqual(f_bs_min_u, 3024, 0)  # f_bs_min_o: 3024 N

        # f_u: Peripheral driving force on driving pulley
        f_u = f_h + f_n + f_s + f_st
        self.assertAlmostEqual(f_u, 13232.32, 2)  # f_u: 13232.32 N

        # Calculate the drive motor power requirements
        p_m = power_requirements.power_requirements_motor(f_u=f_u, v=self.v, d_eta_1=self.d_eta_1, d_eta_2=self.d_eta_2)
        self.assertAlmostEqual(p_m / 1000, 68.93, 2)  # p_m: 68.93 kW

        # Check the min tensile force to transmit f_u (drive pulley)
        t_d_1, t_d_2, t_d_rat = conveyor_resistances.tension_transmit_min(f_u=f_u, wrap_a=self.wrap_a, mu_b=self.mu_b)
        self.assertAlmostEqual(t_d_1, 21680.28, 2)
        self.assertAlmostEqual(t_d_2, 8447.96, 2)
        self.assertTrue(t_d_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Check the min tensile force to avoid belt sag (tail pulley)
        t_t_1, t_t_2, t_t_rat = conveyor_resistances.tension_transmit_min(f_u=f_u, wrap_a=self.wrap_a, mu_b=self.mu_b, t_2_min=f_bs_min_o)
        self.assertAlmostEqual(t_t_1, 35237.40, 2)
        self.assertAlmostEqual(t_t_2, 22005.08, 2)
        self.assertFalse(t_t_rat[2])  # (t_1 / t_2) >= e**(mu_b * wrap_rad)

        # Calculate precise values for wrap resistance using ISO 5048
        # Drive pulley tension
        f_1t_d = conveyor_resistances.resistance_belt_wrap_iso(B=self.B, d=self.d, D=self.D_d, d_0=self.d_0_d,
                                                               m_p=self.m_p_d, t_1=t_t_1, t_2=t_t_2)
        self.assertAlmostEqual(f_1t_d, 153, 0)  # 153 N

        # Tail pulley tension
        f_1t_t = conveyor_resistances.resistance_belt_wrap_iso(B=self.B, d=self.d, D=self.D_t, d_0=self.d_0_t,
                                                               m_p=self.m_p_t, t_1=t_t_2, t_2=t_t_2)
        self.assertAlmostEqual(f_1t_t, 141, 0)  # 141 N

        # Recalculate resistances
        f_n = conveyor_resistances.resistance_secondary(q_v=q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                        B=self.B, b1=self.b1, mu1=self.mu1, mu2=self.mu2,
                                                        wrap_a_h=self.wrap_a, wrap_a_t=self.wrap_a,
                                                        f_1t_d=f_1t_d, f_1t_t=f_1t_t)
        f_n_expected = 5751  # f_n: 5751 N
        self.assertAlmostEqual(f_n, f_n_expected, 0)
        # Sum previous components together
        self.assertAlmostEqual(f_ba + f_f + f_1t_d + f_1t_t, f_n_expected, 0)

        # f_u: Peripheral driving force on driving pulley
        f_u = f_h + f_n + f_s + f_st
        self.assertAlmostEqual(f_u, 12806, 0)  # f_u: 12806 N

        # Recalculate the drive motor power requirements
        p_m = power_requirements.power_requirements_motor(f_u=f_u, v=self.v, d_eta_1=self.d_eta_1, d_eta_2=self.d_eta_2)
        self.assertAlmostEqual(p_m / 1000, 66.71, 2)  # p_m: 68.93 kW
