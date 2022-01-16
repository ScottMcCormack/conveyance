def resistance_main(q_m, q_b, q_ro, q_ru, c_l, install_a, ff):
    """
    Calculate the main resistance (Fh)

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


    """