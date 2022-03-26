def mass_density_material(v, q=None, q_v=None, p=None):
    """
    Calculate the mass of material on the conveyor (kg/m)

    In addition to providing `v`, it accepts either
    a throughput `q` or `q_v` flow rate and `p` material density

    Parameters
    ----------
    v: float
        Speed of the conveyor belt (m/s)
    q: float
        Throughput of the conveyor (t/h)
    q_v: float
        Flow rate of the conveyor (m^3/s)
    p: float
        Density of the material (t/m^3)

    Returns
    -------
    float:
        Mass per metre of material carried (kg/m)

    """
    if q:
        # Given throughput (t/h) and belt speed (m/s)
        q_m = (1000 * q) / (3600 * v)
    else:
        # Given flow rate, material density (t/m^3) and belt speed (m/s)
        q_m = q_v * p * 1000 / v

    return q_m


def mass_density_idler(a, m):
    """
    Calculate the mass of the idler per meter (kg/m)

    Parameters
    ----------
    a: float
        Idler spacing (m)
    m: float
        Idler mass (kg)

    Returns
    -------
    float:
        Mass per meter from idlers (kg/m)

    """
    q = m / a
    return q
