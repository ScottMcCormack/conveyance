import math


def resistance_main(q_m, q_b, q_ro, q_ru, c_l, install_a, ff):
    """
    Calculate the conveyor main resistance (:math:`F_H`)

    Includes the rotational resistances of the carry and return strands, identified by the friction coefficient

        .. math::
            F_H = f * L * g * (q_{ro} + q_{ru} + (2 * q_b + q_m) \\cos \\delta)

    Parameters
    ----------
    q_m: float
        :math:`q_m` : Mass per metre of material carried (:math:`kg/m`)
    q_b: float
        :math:`q_b` : Belt mass per meter (:math:`kg/m`)
    q_ro: float
        :math:`q_{ro}` : Mass of carry idler per meter (:math:`kg/m`)
    q_ru: float
        :math:`q_{ru}` : Mass of return idler per meter (:math:`kg/m`)
    c_l: float
        :math:`L` : Center-to-centre length of the conveyor (:math:`m`)
    install_a: float
        :math:`\\delta` : Installation angle of the conveyor (:math:`deg`)
    ff: float, default=0.02
        :math:`f` : Artificial friction factor (average operating conditions)

    Returns
    -------
    float
        :math:`F_H` : Main resistances to motion (:math:`N`)

    """
    f_h = ff * c_l * 9.81 * (q_ro + q_ru + (2 * q_b + q_m) * math.cos(math.radians(install_a)))
    return f_h


def resistance_secondary(q_v, p, v, v_0, B, b1, mu1, mu2, wrap_a_h, wrap_a_t,
                         f_1t_d=None, f_1t_t=None):
    """
    Calculate the conveyor secondary resistances (:math:`F_N`)

        .. math::
            F_N = F_{bA} + F_f + F_1 + F_t

    Parameters
    ----------
    q_v : float
        :math:`q_v` : Volume per second of material carried (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    v_0 : float
        :math:`v_0` : Speed of the material dropped on to the belt, in the direction of the belt movement (:math:`m/s`)
    B:  float
        :math:`B` : Total width of belt (:math:`m`)
    b1 : float
        :math:`b_1` : Width between skirtplates (:math:`m`)
    mu1 : float
        :math:`\\mu_1` : Friction coefficient between material/belt
    mu2 : float
        :math:`\\mu_2` : Friction coefficient between material/skirtplates
    wrap_a_h : float
        :math:`\\theta_h` : Wrap angle around the head pulley (:math:`deg`)
    wrap_a_t : float
        :math:`\\theta_t` : Wrap angle around the tail pulley (:math:`deg`)
    f_1t_d : float, optional
        :math:`f_{1t,d}` : Wrap resistance between the belt and the drive pulley (:math:`N`)
    f_1t_t : float, optional
        :math:`f_{1t,t}` : Wrap resistance between the belt and the tail pulley (:math:`N`)

    Returns
    -------
    float
        :math:`F_N` : Secondary resistances due to inertial and material and belt frictions (:math:`N`)

    """
    # Inertial and friction resistances (FbA)
    f_ba = resistance_inertial_friction(q_v=q_v, p=p, v=v, v_0=v_0)

    # Resistance between handled material and skirtplates in acceleration area (Ff)
    f_f = resistance_material_acceleration(q_v=q_v, p=p, v=v, v_0=v_0,
                                           b1=b1, mu1=mu1, mu2=mu2)

    # Wrap resistance between the belt and the pulleys (F1t)
    if not f_1t_d:
        f_1t_d = resistance_belt_wrap(B=B, wrap_a=wrap_a_h)  # Drive pulley
    if not f_1t_t:
        f_1t_t = resistance_belt_wrap(B=B, wrap_a=wrap_a_t)  # Tail pulley

    f_n = f_ba + f_f + f_1t_d + f_1t_t
    return f_n


def resistance_concentrated(q_v, p, v, l_s, b1, bc_w, bc_t, bc_p, bc_n, mu2, mu3):
    """
    Calculate concentrated local resistances on the conveyor (:math:`N`)

        .. math::
            F_S = F_{\\epsilon} + F_{gL} + F_{rc} + F_a

    Parameters
    ----------
    q_v : float
        :math:`q_v` : Volume per second of material carried (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    l_s : float
        :math:`l_s` : Length of installation fitted with skirtplates (:math:`m`)
    b1 : float
        :math:`b_1` : Width between skirtplates (:math:`m`)
    bc_w : float
        :math:`bc_w` : Belt cleaner width (:math:`m`)
    bc_t : float
        :math:`bc_t` : Belt cleaner thickness (:math:`m`)
    bc_p : float
        :math:`bc_p` : Pressure between cleaner and belt (:math:`N/m^2`)
    bc_n : int
        :math:`bc_n` : Number of belt cleaners
    mu2 : float
        :math:`\\mu_2` : Friction coefficient between material/skirtplates
    mu3 : float
        :math:`\\mu_3` : Friction coefficient between belt and cleaner

    Returns
    -------
    float
        :math:`F_S` : Conveyor concentrated resistances (:math:`N`)

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
    Calculate the gravity forces from the conveyed material on the belt (:math:`F_N`)

    Parameters
    ----------
    q_m : float
        :math:`q_m` : Mass per metre of material carried (:math:`kg/m`)
    H : float
        :math:`H` : The conveyor lift (:math:`m`)

    Returns
    -------
    float
        :math:`F_N` : Resistance due to gravity of the conveyed material (:math:`N`)

    """
    f_st = q_m * H * 9.81
    return f_st


def resistance_inertial_friction(q_v, p, v, v_0):
    """
    Calculate the inertial and friction resistances (:math:`F_{bA}`)

    Determined at the loading point and in the acceleration area between the material handled and the belt.

    Parameters
    ----------
    q_v : float
        :math:`q_v` : Volume per second of material carried (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    v_0 : float
        :math:`v_0` : Speed of the material dropped on to the belt, in the direction of the belt movement (:math:`m/s`)

    Returns
    -------
    float
        (:math:`F_{bA}`) : Resistance due to inertial and friction forces (:math:`N`)

    """
    f_ba = q_v * p * 1000 * (v - v_0)
    return f_ba


def resistance_material_acceleration(q_v, p, v, v_0, b1, mu1, mu2):
    """
    Calculate the resistance between handled material and skirtplates in acceleration area (:math:`F_f`)

    Parameters
    ----------
    q_v : float
        :math:`q_v` : Volume per second of material carried (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    v_0 : float
        :math:`v_0` : Speed of the material dropped on to the belt, in the direction of the belt movement (:math:`m/s`)
    b1 : float
        :math:`b_1` : Width between skirtplates (:math:`m`)
    mu1 : float
        :math:`\\mu_1` : Friction coefficient between material/belt
    mu2 : float
        :math:`\\mu_2` : Friction coefficients between material/skirtplates

    Returns
    -------
    float
        :math:`F_f` : Resistance between handled material and skirtplates in acceleration area (:math:`N`)

    """
    g = 9.81
    i_bmin = (v ** 2 - v_0 ** 2) / (2 * g * mu1)
    f_f = (mu2 * q_v ** 2 * p * 1000 * g * i_bmin) / (((v + v_0) / 2) ** 2 * b1 ** 2)
    return f_f


def resistance_belt_wrap(B, wrap_a):
    """
    Calculate the wrap resistance between the belt and pulley (:math:`F_{1t}`)

    Parameters
    ----------
    B : float
        :math:`B` : Total width of belt (:math:`m`)
    wrap_a : float
        :math:`\\theta` : Wrap angle around the pulley (:math:`\\theta`)

    Returns
    -------
    float
        :math:`F_{1t}` : Resistance between the belt and pulley (:math:`N`)

    """
    # If alpha > 90, then sin(alpha) = 1
    alpha = max([180 - wrap_a, 90])

    f_1t = 300 * B * math.sin(math.radians(alpha))
    return f_1t


def resistance_material_skirtplates(q_v, p, v, l_s, b1, mu2):
    """
    Calculate the resistance due to friction between the material handled and skirt plates (:math:`F_{gL}`)

    Parameters
    ----------
    q_v : float
        :math:`q_v` : Volume per second of material carried (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    l_s : float
        :math:`l_s` : Length of installation fitted with skirtplates (:math:`m`)
    b1 : float
        :math:`b_1` : Width between skirtplates (:math:`m`)
    mu2 : float
        :math:`\\mu_2` : Friction coefficients between material/skirtplates

    Returns
    -------
    float
        :math:`F_{gL}`: Resistance due to friction between the material handled and skirt plates (:math:`N`)

    """
    f_gl = (mu2 * (q_v ** 2) * (p * 1000) * 9.81 * l_s) / ((v ** 2) * (b1 ** 2))
    return f_gl


def resistance_belt_cleaners(bc_w, bc_t, bc_p, bc_n, mu3):
    """
    Calculate the friction resistance due to belt cleaners fitted to the conveyor (:math:`F_{rc}`)

    Parameters
    ----------
    bc_w : float
        :math:`bc_{w}` : Belt cleaner width (:math:`m`)
    bc_t : float
        :math:`bc_{t}` : Belt cleaner thickness (:math:`m`)
    bc_p : float
        :math:`bc_{p}` : Pressure between cleaner and belt (:math:`N/m^2`)
    bc_n : int
        :math:`bc_{n}` : Number of belt cleaners
    mu3 : float
        :math:`\\mu_2` : Friction coefficient between belt and cleaner

    Returns
    -------
    float
        :math:`F_{rc}` : Friction resistance due to belt cleaners fitted to the conveyor (:math:`N`)

    """
    f_rc = bc_w * bc_t * bc_p * bc_n * mu3
    return f_rc


def resistance_belt_sag_tension(q_m, q_b, a_o, a_u, h_a_o, h_a_u):
    """
    Calculate the minimum tensile force to limit belt sag between 2 sets of idlers on the carry side

    Parameters
    ----------
    q_m : float
        :math:`q_m` : Mass per metre of material carried (:math`kg/m`)
    q_b : float
        :math:`q_b` : Belt mass per meter (:math`kg/m`)
    a_o : float
        :math:`a_o` : Idler spacing, carry (:math`m`)
    a_u : float
        :math:`a_u` : Idler spacing, return (:math`m`)
    h_a_o : float
        :math:`h_{ao}` : Allowable belt sag between idlers, carry (:math`m`)
    h_a_u : float
        :math:`h_{au}` : Allowable belt sag between idlers, return (:math`m`)

    Returns
    -------
    float
        Carry side, minimum tensile force to limit belt sag between 2 sets of idlers (:math:`N`)
    float
        Return side, minimum tensile force to limit belt sag between 2 sets of idlers (:math:`N`)

    """
    # Carry side
    f_bs_min_o = (a_o * (q_b + q_m) * 9.81) / (8 * h_a_o)

    # Return side
    f_bs_min_u = (a_u * q_b * 9.81) / (8 * h_a_u)

    return f_bs_min_o, f_bs_min_u


def resistance_belt_wrap_iso(B, d, D, d_0, m_p, t_1, t_2):
    """
    Calculate belt wrap resistance using values from ISO 5048

        .. math::
            F_T    & = ((T_1 + T_2) * (g * m_p))^{1/2} \\\\
            F_t    & = 0.005 * (d_0 / D) * F_T \\\\
            F_1    & = 9 * B * (140 + 0.01 (T / B) * d / D \\\\
            F_{1t} & = F_1 + F_t

    Where:
        :math:`F_1` : Wrap resistance between belt and pulley (:math:`N`);
        :math:`F_t` : Pulley bearing resistance (:math:`N`)

    Parameters
    ----------
    B : float
        :math:`B` : Total width of belt (:math:`m`)
    d : float
        :math:`d` : Belt thickness (:math:`m`)
    d_0 : float
        :math:`d_0` : Inside bearing diameter (:math:`m`)
    D : float
        :math:`D` : Pulley diameter (:math:m`)
    m_p : float
        :math:`m_p` : Pulley mass (:math:`kg`)
    t_1 : float
        :math:`T_1` : Tight-side tension at pulley (:math:`N`)
    t_2 : float
        :math:`T_2` : Slack-side tension at pulley (:math:`N`)

    Returns
    -------
    float
        :math:`F_{1t}`: Approximate combined resistance (:math:`N`)

    """
    g = 9.81
    # F: Average belt tension at the pulley
    F = (t_1 + t_2) / 2

    # f_1: Wrap resistance between belt and pulley
    f_1 = 9 * B * (140 + (0.01 * F / B)) * d / D

    # f_t: Pulley bearing resistance
    f_t = 0.005 * (d_0 / D) * (((t_1 + t_2) ** 2) + (g * m_p) ** 2) ** (1 / 2)
    return f_1 + f_t


def tension_transmit_min(f_u, wrap_a, mu_b, acc_sd=3, t_2_min=None):
    """
    Ensure that a minimum tensile force is sufficient to transmit :math:`f_u`

    The following ratio should be satisfied.

        .. math::
            (t_1 / t_2) \\leq \\exp(\\mu_b * \\alpha)

    Parameters
    ----------
    f_u :  float
        :math:`f_u` : Peripheral driving force on driving pulley (:math:`N`)
    wrap_a : float
        :math:`\\alpha` : Wrap angle around the pulley (:math:`\\theta`)
    mu_b : float
        :math:`\\mu_b` : Belt/Pulley friction coefficient
    acc : int, optional
        Significant digit accuracy for checking the ratio (default: 3)
    t_2_min : float, optional
        :math:`t_2` : Minimum tensile force that must be maintained to transmit :math:`f_u`

    Returns
    -------
    float
        :math:`t_1` : Tight-side tension at pulley (:math:`N`)
    float
        :math:`t_2` : Slack-side tension at pulley (:math:`N`)
    tuple
        :math:`(x,  y, z), where\\ x = (t_1 / t_2)\\ y = \\exp(\\mu_b * \\alpha)\\ z = (t_1 / t_2) \\leq \\exp(\\mu_b * \\alpha)`

    """
    wrap_rad = wrap_a * (math.pi / 180)
    t_d_rat_min = math.exp(mu_b * wrap_rad)

    # Set a value for t_2_min if not set
    if t_2_min is None:
        t_2_min = f_u / (t_d_rat_min - 1)

    # t_1: Tight side tension at pulley
    t_1 = f_u + t_2_min

    # Ensure the ratio (t_1 / t_2_min) >= e(mu_b * wrap_rad)
    t_d_rat = t_1 / t_2_min
    t_d_min_ok = round(t_d_rat, ndigits=acc_sd) >= round(t_d_rat_min, ndigits=acc_sd)

    return t_1, t_2_min, (t_d_rat, t_d_rat_min, t_d_min_ok)
