def power_requirements_motor(f_u, v, d_eta_1, d_eta_2):
    """
    Calculate the power requirements for the drive motor (P\ :sub:`A`\)


    Parameters
    ----------
    f_u: float
       f\ :sub:`u`\  : Peripheral driving force on driving pulley (N)
    v: float
        v : Speed of the conveyor belt (m/s)
    d_eta_1: float
        Fluid coupling efficiency
    d_eta_2: float
        Gearbox efficiency


    Returns
    -------
    float:
        Power requirements for the drive motor (W)

    """
    # p_a: Drive pulley power requirements (operating requirements)
    p_a = f_u * v

    # Drive efficiency
    d_eta = d_eta_1 * d_eta_2

    # p_a: Drive motor power requirements
    p_m = p_a / d_eta
    return p_m
