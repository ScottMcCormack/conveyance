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
        Coefficients between material/belt
    mu2: float
        Coefficients between material/skirtplates
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
        Coefficients between material/belt
    mu2: float
        Coefficients between material/skirtplates

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
    alpha = 180 - wrap_a
    f_1t = 300 * B * math.sin(math.radians(alpha))
    return f_1t
