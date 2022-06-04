import yaml

from conveyance import belt_capacity, conveyor_resistances, power_requirements


class Conveyance:
    """Class used for conveyor design.

    .. versionadded:: 0.1.0

    Attributes
    ----------
    file_path : str
        Path to file containing the design parameters for the conveyor.
    q : float
        Target capacity

    """

    def __init__(self, file_path, q):
        self.q = q

        # Load design parameters
        self._file_loader(file_path=file_path)

        # Calculate cross-section
        self._calculate_cross_sectional_capacity()

        # Calculate conveyor design
        self._calculate_conveyor_design()

    def calculate_iso_method(self):
        """Calculate using the ISO method

        """
        # Min tensile force to transmit f_u (drive pulley)
        self.t_d_1, self.t_d_2, self.t_d_rat = conveyor_resistances.tension_transmit_min(f_u=self.f_u, wrap_a=self.wrap_a, mu_b=self.mu_b)

        # Min tensile force to avoid belt sag (tail pulley)
        self.t_t_1, self.t_t_2, self.t_t_rat = conveyor_resistances.tension_transmit_min(f_u=self.f_u, wrap_a=self.wrap_a, mu_b=self.mu_b,
                                                                                         t_2_min=self.f_bs_min_o)
        # Drive pulley tension
        self.f_1t_d = conveyor_resistances.resistance_belt_wrap_iso(B=self.B, d=self.d, D=self.D_d, d_0=self.d_0_d,
                                                                    m_p=self.m_p_d, t_1=self.t_t_1, t_2=self.t_t_2)

        # Tail pulley tension
        self.f_1t_t = conveyor_resistances.resistance_belt_wrap_iso(B=self.B, d=self.d, D=self.D_t, d_0=self.d_0_t,
                                                                    m_p=self.m_p_t, t_1=self.t_t_2, t_2=self.t_t_2)

        # Calculate secondary resistance
        self.f_n = conveyor_resistances.resistance_secondary(q_v=self.q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                             B=self.B, b1=self.b1, mu1=self.mu1, mu2=self.mu2,
                                                             wrap_a_h=self.wrap_a, wrap_a_t=self.wrap_a,
                                                             f_1t_d=self.f_1t_d, f_1t_t=self.f_1t_t)

        # f_u: Peripheral driving force on driving pulley
        self.f_u = self.f_h + self.f_n + self.f_s + self.f_st

        # Recalculate the drive motor power requirements
        self.p_m = power_requirements.power_requirements_motor(f_u=self.f_u, v=self.v, d_eta_1=self.d_eta_1, d_eta_2=self.d_eta_2)

    def _file_loader(self, file_path):
        """Load the design parameters from a YAML file.

        .. versionadded:: 0.1.0

        Parameters
        ----------
        file_path : str
            Path to YAML file

        """
        with open(file_path, 'r') as stream:
            d: dict = yaml.safe_load(stream=stream)

        # Load objects from file
        c_d = d['conveyor_design']

        # conveyor_design
        mat = c_d['material']
        op = c_d['operation']
        coef = c_d['coefficients']
        belt = c_d['belt']
        drive_pulley = c_d['pulley']['drive']
        tail_pulley = c_d['pulley']['tail']
        carry_idler = c_d['idler']['carry']
        return_idler = c_d['idler']['return']
        sk_p = c_d['skirtplates']
        b_c = c_d['belt_cleaners']

        # Assume 3-roll configuration using coal
        self.l3 = carry_idler['l3']  # Width of the idler (3 roll set)
        self.B = belt['B']  # Total width of the belt (m)
        self.d = belt['d']  # Thickness of the belt (m)
        self.b = belt['b']  # Width of max material on belt (m)
        self.ia = carry_idler['ia']  # Idlers angle (deg)
        self.sa = mat['sa']  # Material surcharge angle, coal (deg)
        self.b1 = sk_p['b1']  # Width between skirtplates (m)
        self.l_s = sk_p['l_s']  # Length of installation fitted with skirtplates (m)

        # Vars for mass_density_material
        self.v = op['v']  # Belt speed (m/s)
        self.v_0 = op['v_0']  # Speed of conveyed material (m/s)
        self.p = mat['p']  # Density, coal (t/m^3)
        # self.q_v = 0.864  # (m^3/s)
        # self.q = 2300  # (t/h)

        # Vars for idlers
        self.a_o = carry_idler['a_o']  # Carry idler spacing (m)
        self.m_o = carry_idler['m_o']  # Carry idler mass (kg)
        self.h_a_o = carry_idler['h_a_o']  # Allowable belt sag, carry side (m)
        self.a_u = return_idler['a_u']  # Return idler spacing (m)
        self.m_u = return_idler['m_u']  # Return idler mass (kg)
        self.h_a_u = return_idler['h_a_u']  # Allowable belt sag, return side (m)

        # Vars for conveyor resistances
        self.q_b = belt['q_b']  # Belt mass (kg/m)
        self.c_l = op['c_l']  # Center-to-centre length of the conveyor (m)
        self.install_a = op['install_a']  # Installation angle of the conveyor (deg)
        self.wrap_a = op['wrap_a']  # Wrap angle around the pulley (deg)
        self.ff = coef['ff']  # Artificial friction factor (average operating conditions)
        self.mu1 = coef['mu1']  # Coefficients between material/belt
        self.mu2 = coef['mu2']  # Coefficients between material/skirtplates

        # Vars for belt cleaners
        self.bc_w = b_c['bc_w']  # Belt cleaner width (m)
        self.bc_t = b_c['bc_t']  # Belt cleaner thickness (m)
        self.bc_p = b_c['bc_p']  # Pressure between cleaner and belt
        self.bc_n = b_c['bc_n']  # Number of belt cleaners (three at head end, one at tail end)
        self.mu3 = coef['mu3']  # Friction coefficient between belt and cleaner

        # Vars for drive pulley
        self.d_eta_1 = coef['d_eta_1']  # Fluid coupling efficiency
        self.d_eta_2 = coef['d_eta_2']  # Gearbox efficiency
        self.mu_b = coef['mu_b']  # Belt/Pulley friction coefficient
        self.d_0_d = drive_pulley['d_0']  # Diameter of inside bearing
        self.D_d = drive_pulley['D']  # Drive pulley diameter
        self.m_p_d = drive_pulley['m_p']  # Drive pulley mass

        # Vars for tail pulley
        self.d_0_t = tail_pulley['d_0']  # Diameter of inside bearing
        self.D_t = tail_pulley['D']  # Tail pulley diameter
        self.m_p_t = tail_pulley['m_p']  # Tail pulley mass

    def _calculate_cross_sectional_capacity(self):
        """Calculate the cross-sectional properties of the conveyor

        """
        self.s = belt_capacity.belt_cs_area(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.q_vt = belt_capacity.volumetric_flow(belt_ca=self.s, v=self.v)
        self.q_mt = belt_capacity.mass_density_material(v=self.v, q_v=self.q_vt, p=self.p)

    def _calculate_conveyor_design(self):
        """Calculate the design of the conveyor

        """
        self.q_m = belt_capacity.mass_density_material(v=self.v, q=self.q)
        self.q_ro = belt_capacity.mass_density_idler(a=self.a_o, m=self.m_o)
        self.q_ru = belt_capacity.mass_density_idler(a=self.a_u, m=self.m_u)

        # Fh: Conveyor main resistance
        self.f_h = conveyor_resistances.resistance_main(q_m=self.q_m, q_b=self.q_b, q_ro=self.q_ro, q_ru=self.q_ru,
                                                        c_l=self.c_l, install_a=self.install_a, ff=self.ff)

        # Fst: Resistance due to gravity of the conveyed material
        self.f_st = conveyor_resistances.resistance_gravity(q_m=self.q_m, H=0)

        # Fba: Resistance due to inertial and frictional forces
        self.q_v = belt_capacity.volume_carried_material(q=self.q, p=self.p)
        self.f_ba = conveyor_resistances.resistance_inertial_friction(q_v=self.q_v, p=self.p, v=self.v, v_0=self.v_0)

        # Ff: Resistance between handled material and skirtplates in acceleration area
        self.f_f = conveyor_resistances.resistance_material_acceleration(q_v=self.q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                                         b1=self.b1, mu1=self.mu1, mu2=self.mu2)

        # f_1t: Wrap resistance between the belt and the pulleys
        self.f_1t = conveyor_resistances.resistance_belt_wrap(B=self.B, wrap_a=self.wrap_a)

        # f_n: Calculate secondary resistances (Fn)
        self.f_n = conveyor_resistances.resistance_secondary(q_v=self.q_v, p=self.p, v=self.v, v_0=self.v_0,
                                                             B=self.B, b1=self.b1, mu1=self.mu1, mu2=self.mu2,
                                                             wrap_a_h=self.wrap_a, wrap_a_t=self.wrap_a)

        # f_gl: Resistance due to friction between the material handled and skirt plates
        self.f_gl = conveyor_resistances.resistance_material_skirtplates(q_v=self.q_v, p=self.p, v=self.v, l_s=self.l_s, b1=self.b1,
                                                                         mu2=self.mu2)

        # Determine belt sag tension force
        self.f_bs_min_o, self.f_bs_min_u = conveyor_resistances.resistance_belt_sag_tension(q_m=self.q_m, q_b=self.q_b, a_o=self.a_o, a_u=self.a_u,
                                                                                            h_a_o=self.h_a_o, h_a_u=self.h_a_u)

        # f_rc: Friction resistance due to belt cleaners fitted to the conveyor
        self.f_rc = conveyor_resistances.resistance_belt_cleaners(bc_w=self.bc_w, bc_t=self.bc_t, bc_p=self.bc_p,
                                                                  bc_n=self.bc_n, mu3=self.mu3)

        # f_s: Special resistances
        self.f_s = conveyor_resistances.resistance_concentrated(q_v=self.q_v, p=self.p, v=self.v, l_s=self.l_s, b1=self.b1,
                                                                bc_w=self.bc_w, bc_t=self.bc_t, bc_p=self.bc_p,
                                                                bc_n=self.bc_n, mu3=self.mu3, mu2=self.mu2)

        # f_u: Peripheral driving force on driving pulley
        self.f_u = self.f_h + self.f_n + self.f_s + self.f_st

        # Calculate the drive motor power requirements
        self.p_m = power_requirements.power_requirements_motor(f_u=self.f_u, v=self.v, d_eta_1=self.d_eta_1, d_eta_2=self.d_eta_2)
