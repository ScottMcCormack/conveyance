import math


def mass_density_material(v, q=None, q_v=None, p=None):
    """
    Calculate the mass of material on the conveyor (:math:`kg/m`)

    In addition to providing `v`, it accepts either a throughput
    :math:`q` or :math:`q_v` flow rate and :math:`p` material density

    Parameters
    ----------
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    q : float
        :math:`q` : Throughput of the conveyor (:math:`t/h`)
    q_v : float
        :math:`q_v` : Flow rate of the conveyor (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)

    Returns
    -------
    float
        Mass per metre of material carried (:math:`kg/m`)

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
    Calculate the mass of the idler per meter (:math:`kg/m`)

    Parameters
    ----------
    a : float
        :math:`a` : Idler spacing (:math:`m`)
    m : float
        :math:`m` : Idler mass (:math:`kg`)

    Returns
    -------
    float
        Mass per meter from idlers (:math:`kg/m`)

    """
    q = m / a
    return q


def volume_carried_material(q, p):
    """
    Calculate the volume carried per second (:math:`m^3/s`)

    Parameters
    ----------
    q : float
        :math:`q` : Throughput of the conveyor (:math:`t/h`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)

    Returns
    -------
    float
        Volume per second of material carried (:math:`m^3/s`)

    """
    q_v = (1000 * q) / (3600 * p * 1000)
    return q_v


def volumetric_flow(belt_ca, v):
    """
    Calculate the theoretical flow rate of the conveyor

    Parameters
    ----------
    belt_ca : float
        Cross-sectional area of material of the belt (:math:`m^2`)
    v : float
        Speed of the conveyor belt (:math:`m/s`)

    Returns
    -------
    float
        The theoretical flow rate of the conveyor (:math:`m^3/s`)

    """
    return belt_ca * v


def belt_cs_area(l3, b, ia, sa):
    """
    Calculate the cross-sectional area of material of the belt.

    A three-roll idler set is assumed.

    Parameters
    ----------
    l3 : float
        :math:`l_3` : Width of the idler (:math:`m`)
    b : float
        :math:`b` : Width of max material on belt (:math:`m`)
    ia : float
        :math:`i_a` : Installed angle of the side idlers (:math:`\\theta`)
    sa : float
        :math:`s_a` : Surcharge angle of the material (:math:`\\theta`)

    Returns
    -------
    float
        The cross-sectional area of material on the belt (:math:`m^2`)

    """
    # Convert deg inputs to radians
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)

    # Upper half of the belt
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)

    # Lower half of the belt
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s1 + s2
