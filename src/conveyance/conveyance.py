import yaml


class Conveyance:
    def __init__(self, file_path):
        # Load from file
        self.file_loader(file_path=file_path)

    def file_loader(self, file_path):
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
