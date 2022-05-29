def power_requirements_motor(f_u, v, d_eta_1, d_eta_2):
    """
    Calculate the power requirements for the drive motor (:math:`P_A`)

        .. math::
            P_A = \\dfrac{F_u\\ v}{\\eta_1\\ \\eta_2}

    Parameters
    ----------
    f_u : float
       :math:`F_u` : Peripheral driving force on driving pulley (:math:`N`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    d_eta_1 : float
        :math:`\\eta_1` : Fluid coupling efficiency
    d_eta_2 : float
        :math:`\\eta_2` : Gearbox efficiency

    Returns
    -------
    float
        :math:`P_A` : Power requirements for the drive motor (:math:`W`)

    """
    # p_a: Drive pulley power requirements (operating requirements)
    p_a = f_u * v

    # Drive efficiency
    d_eta = d_eta_1 * d_eta_2

    # p_a: Drive motor power requirements
    p_m = p_a / d_eta
    return p_m
