import math


def resistance_main(q_m, q_b, q_ro, q_ru, c_l, install_a, ff):
    """
    Calculate the conveyor main resistance (Fh)

    Includes the rotational resistances of the carry and return strands, identified by friction coefficient

    Parameters
    ----------
    q_m: float
        Mass per metre of material carried (kg/m)
    q_b: float
        Belt mass per meter (kg/m)
    q_ro: float
        Mass of carry idler per meter (kg/m)
    q_ru: float
        Mass of return idler per meter (kg/m)
    c_l: float
        Center-to-centre length of the conveyor (m)
    install_a: float
        Installation angle of the conveyor (deg)
    ff: float, default=0.02
        Artificial friction factor (average operating conditions)

    Returns
    -------
    float:
        Main resistances to motion (N)

    """
    f_h = ff * c_l * 9.81 * (q_ro + q_ru + (2 * q_b + q_m) * math.cos(math.radians(install_a)))
    return f_h


def resistance_secondary(q_v, p, v, v_0, B, b1, mu1, mu2, wrap_a_h, wrap_a_t):
    """
    Calculate the conveyor secondary resistances (Fn)

    Parameters
    ----------
    q_v: float
        Volume per second of material carried (m^3/s)
    p: float
        Density of the material (t/m^3)
    v: float
        Speed of the conveyor belt (m/s)
    v_0: float
        Speed of the material dropped on to the belt, in the direction of the belt movement (m/s)
    B: float
        Total width of belt (m)
    b1: float
        Width between skirtplates (m)
    mu1: float
        Friction coefficient between material/belt
    mu2: float
        Friction coefficient between material/skirtplates
    wrap_a_h: float
        Wrap angle around the head pulley (deg)
    wrap_a_t: float
        Wrap angle around the tail pulley (deg)

    Returns
    -------
    float:
        Secondary resistances due to inertial and material and belt frictions (N)

    """
    # Inertial and friction resistances (FbA)
    f_ba = resistance_inertial_friction(q_v=q_v, p=p, v=v, v_0=v_0)

    # Resistance between handled material and skirtplates in acceleration area (Ff)
    f_f = resistance_material_acceleration(q_v=q_v, p=p, v=v, v_0=v_0,
                                           b1=b1, mu1=mu1, mu2=mu2)

    # Wrap resistance between the belt and the pulleys (F1t)
    f_1t_h = resistance_belt_wrap(B=B, wrap_a=wrap_a_h)  # Head pulley
    f_1t_t = resistance_belt_wrap(B=B, wrap_a=wrap_a_t)  # Tail pulley

    f_n = f_ba + f_f + f_1t_h + f_1t_t
    return f_n


def resistance_concentrated(q_v, p, v, l_s, b1, bc_w, bc_t, bc_p, bc_n, mu2, mu3):
    """
    Calculate concentrated local resistances on the conveyor

    Parameters
    ----------
    q_v: float
        Volume per second of material carried (m^3/s)
    p: float
        Density of the material (t/m^3)
    v: float
        Speed of the conveyor belt (m/s)
    l_s: float
        Length of installation fitted with skirtplates (m)
    b1: float
        Width between skirtplates (m)
    bc_w: float
        Belt cleaner width (m)
    bc_t: float
        Belt cleaner thickness (m)
    bc_p : float
        Pressure between cleaner and belt (N/m^2)
    bc_n : int
        Number of belt cleaners
    mu2: float
        Friction coefficient between material/skirtplates
    mu3: float
        Friction coefficient between belt and cleaner

    Returns
    -------
    float:
        Conveyor concentrated resistances (N)

    """
    # Resistance due to idler tilting (Fep)
    f_ep = 0  # No idler tilting

    # Resistance due to friction between the material handled and skirt plates (FgL)
    f_gl = resistance_material_skirtplates(q_v=q_v, p=p, v=v, l_s=l_s, b1=b1, mu2=mu2)

    # Resistance due to belt cleaners fitted to the conveyor (Frc)
    f_rc = resistance_belt_cleaners(bc_w=bc_w, bc_t=bc_t, bc_p=bc_p, bc_n=bc_n, mu3=mu3)

    # Resistance due to friction at a discharge plough (Fa)
    f_a = 0  # No discharge ploughs present

    f_s = f_ep + f_gl + f_rc + f_a
    return f_s


def resistance_gravity(q_m, H):
    """
    Calculate the gravity forces from the conveyed material on the belt (FN)

    Parameters
    ----------
    q_m: float
        Mass per metre of material carried (kg/m)
    H: float
        The conveyor lift (m)

    Returns
    -------
    float:
        Resistance due to gravity of the conveyed material (N)

    """
    f_st = q_m * H * 9.81
    return f_st


def resistance_inertial_friction(q_v, p, v, v_0):
    """
    Calculate the inertial and friction resistances (FbA)

    Determined at the loading point and in the acceleration area between the material handled and the belt (FbA)

    Parameters
    ----------
    q_v: float
        Volume per second of material carried (m^3/s)
    p: float
        Density of the material (t/m^3)
    v: float
        Speed of the conveyor belt (m/s)
    v_0: float
        Speed of the material dropped on to the belt, in the direction of the belt movement (m/s)


    Returns
    -------
    float:
        Resistance due to inertial and friction forces (N)

    """
    f_ba = q_v * p * 1000 * (v - v_0)
    return f_ba


def resistance_material_acceleration(q_v, p, v, v_0, b1, mu1, mu2):
    """
    Calculate the resistance between handled material and skirtplates in acceleration area (Ff)

    Parameters
    ----------
    q_v: float
        Volume per second of material carried (m^3/s)
    p: float
        Density of the material (t/m^3)
    v: float
        Speed of the conveyor belt (m/s)
    v_0: float
        Speed of the material dropped on to the belt, in the direction of the belt movement (m/s)
    b1: float
        Width between skirtplates (m)
    mu1: float
        Friction coefficient between material/belt
    mu2: float
        Friction coefficients between material/skirtplates

    Returns
    -------
    float:
        Resistance between handled material and skirtplates in acceleration area (N)

    """
    g = 9.81
    i_bmin = (v ** 2 - v_0 ** 2) / (2 * g * mu1)
    f_f = (mu2 * q_v ** 2 * p * 1000 * g * i_bmin) / (((v + v_0) / 2) ** 2 * b1 ** 2)
    return f_f


def resistance_belt_wrap(B, wrap_a):
    """
    Calculate the wrap resistance between the belt and pulley (F1t)

    Parameters
    ----------
    B: float
        Total width of belt (m)
    wrap_a: float
        Wrap angle around the pulley (deg)

    Returns
    -------
    float:
        Resistance between the belt and pulley (N)

    """
    # If alpha > 90, then sin(alpha) = 1
    alpha = max([180 - wrap_a, 90])

    f_1t = 300 * B * math.sin(math.radians(alpha))
    return f_1t


def resistance_material_skirtplates(q_v, p, v, l_s, b1, mu2):
    """
    Calculate the resistance due to friction between the material handled and skirt plates (FgL)

    Parameters
    ----------
    q_v: float
        Volume per second of material carried (m^3/s)
    p: float
        Density of the material (t/m^3)
    v: float
        Speed of the conveyor belt (m/s)
    l_s: float
        Length of installation fitted with skirtplates (m)
    b1: float
        Width between skirtplates (m)
    mu2: float
        Friction coefficients between material/skirtplates

    Returns
    -------
    float:
        Resistance due to friction between the material handled and skirt plates (N)

    """
    f_gl = (mu2 * (q_v ** 2) * (p * 1000) * 9.81 * l_s) / ((v ** 2) * (b1 ** 2))
    return f_gl


def resistance_belt_cleaners(bc_w, bc_t, bc_p, bc_n, mu3):
    """
    Calculate the friction resistance due to belt cleaners fitted to the conveyor (Frc)

    Parameters
    ----------
    bc_w: float
        Belt cleaner width (m)
    bc_t: float
        Belt cleaner thickness (m)
    bc_p : float
        Pressure between cleaner and belt (N/m^2)
    bc_n : int
        Number of belt cleaners
    mu3: float
        Friction coefficient between belt and cleaner

    Returns
    -------
    float:
        Friction resistance due to belt cleaners fitted to the conveyor (N)

    """
    f_rc = bc_w * bc_t * bc_p * bc_n * mu3
    return f_rc


def resistance_belt_sag_tension(q_m, q_b, a_o, a_u, h_a_o, h_a_u):
    """
    Calculate the minimum tensile force to limit belt sag between 2 sets of idlers on the carry side

    Parameters
    ----------
    q_m: float
        Mass per metre of material carried (kg/m)
    q_b: float
        Belt mass per meter (kg/m)
    a_o: float
        Idler spacing, carry (m)
    a_u: float
        Idler spacing, return (m)
    h_a_o: float
        Allowable belt sag between idlers, carry (m)
    h_a_u: float
        Allowable belt sag between idlers, return (m)

    Returns
    -------
    float:
        Carry side, minimum tensile force to limit belt sag between 2 sets of idlers (N)
    float:
        Return side, minimum tensile force to limit belt sag between 2 sets of idlers (N)

    """
    # Carry side
    f_bs_min_o = (a_o * (q_b + q_m) * 9.81) / (8 * h_a_o)

    # Return side
    f_bs_min_u = (a_u * q_b * 9.81) / (8 * h_a_u)

    return f_bs_min_o, f_bs_min_u


def tension_transmit_min(f_u, wrap_a, mu_b, acc_sd=3, t_2_min=None):
    """
    Ensure that a minimum tensile force is sufficient to transmit f_u

    Parameters
    ----------
    f_u: float
        Peripheral driving force on driving pulley (N)
    wrap_a: float
        Wrap angle around the pulley (deg)
    mu_b: float
        # Belt/Pulley friction coefficient
    acc: int, optional
        # Significant digit accuracy for checking the ratio (default: 3)
    t_2_min: float, optional
        # Minimum tensile force that must be maintained to transmit f_u, optional

    Returns
    -------
    float:
        t_1: Tensile force on belt (N)
    float:
        t_2: Tensile force on belt (N)
    tuple:
        (t_1 / t_2) >= e**(mu_b * wrap_rad)

    """
    wrap_rad = wrap_a * (math.pi / 180)
    t_d_rat_min = math.exp(mu_b * wrap_rad)

    # Set a value for t_2_min if not set
    if t_2_min is None:
        t_2_min = f_u / (t_d_rat_min - 1)

    # t_1: Tensile force on the belt
    t_1 = f_u + t_2_min

    # Ensure the ratio (t_1 / t_2_min) >= e(mu_b * wrap_rad)
    t_d_rat = t_1 / t_2_min
    t_d_min_ok = round(t_d_rat, ndigits=acc_sd) >= round(t_d_rat_min, ndigits=acc_sd)

    return t_1, t_2_min, (t_d_rat, t_d_rat_min, t_d_min_ok)
