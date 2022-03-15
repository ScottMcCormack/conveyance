import math


def resistance_main(q_m, q_b, q_ro, q_ru, c_l, install_a, ff):
    """
    Calculate the main resistance (Fh)

    Includes the rotational resistances of the carry and return strands, identified by friction
    coeffient

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
        Main resistances to motion

    """
    f_h = ff * c_l * 9.81 * (q_ro + q_ru + (2 * q_b + q_m) * math.cos(math.radians(install_a)))
    return f_h
