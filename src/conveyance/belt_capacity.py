import math


def mass_density_material(v, q=None, q_v=None, p=None):
    """
    Calculate the mass of material on the conveyor (:math:`kg/m`)

    In addition to providing `v`, it accepts either a throughput
    :math:`q`

        .. math::
            q_m = \\dfrac{q}{3600\\ v}

    Or :math:`q_v` flow rate and :math:`\\rho` material density

        .. math::
            q_m = \\dfrac{Q_v\\ \\rho}{v}

    Parameters
    ----------
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)
    q : float
        :math:`q` : Throughput of the conveyor (:math:`t/h`)
    q_v : float
        :math:`Q_v` : Flow rate of the conveyor (:math:`m^3/s`)
    p : float
        :math:`\\rho` : Density of the material (:math:`t/m^3`)

    Returns
    -------
    float
        :math:`q_m` : Mass per metre of material carried (:math:`kg/m`)

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

        .. math::
            q_r = \\dfrac{m}{a}

    Parameters
    ----------
    a : float
        :math:`a` : Idler spacing (:math:`m`)
    m : float
        :math:`m` : Idler mass (:math:`kg`)

    Returns
    -------
    float
        :math:`q_r` : Mass per meter from idlers (:math:`kg/m`)

    """
    q = m / a
    return q


def volume_carried_material(q, p):
    """
    Calculate the volume carried per second (:math:`m^3/s`)

        .. math::
            Q_v = \\dfrac{q}{3600\\ \\rho}

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
    Calculate the theoretical flow rate of the conveyor (:math:`m^3/s`)

        .. math::
            Q_v = S\\ v

    Parameters
    ----------
    belt_ca : float
        :math:`S` : Cross-sectional area of material of the belt (:math:`m^2`)
    v : float
        :math:`v` : Speed of the conveyor belt (:math:`m/s`)

    Returns
    -------
    float
        :math:`Q_v` : The theoretical flow rate of the conveyor (:math:`m^3/s`)

    """
    return belt_ca * v


def belt_cs_area(l3, b, ia, sa):
    """
    Calculate the cross-sectional area of material on the belt (:math:`m^2`)

    **Note**: A three-roll idler set is assumed.

        .. math::
            S_1  & = \\frac{1}{6} (l_3 + (b - l_3) \\cos \\lambda)^2 \\tan \\theta \\\\
            S_2  & = \\left (l_3 + \\dfrac {b - l_3}{2} \\cos \\lambda \\right)
                     \\left (\\dfrac {b - l_3}{2} \\sin \\lambda \\right) \\\\
            S    & = S_1 + S_2

    Parameters
    ----------
    l3 : float
        :math:`l_3` : Width of the idler (:math:`m`)
    b : float
        :math:`b` : Width of max material on belt (:math:`m`)
    ia : float
        :math:`\\lambda` : Installed angle of the side idlers (:math:`deg`)
    sa : float
        :math:`\\theta` : Surcharge angle of the material (:math:`deg`)

    Returns
    -------
    float
        :math:`S` : The cross-sectional area of material on the belt (:math:`m^2`)

    """
    # Convert deg inputs to radians
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)

    # Upper half of the belt
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)

    # Lower half of the belt
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s1 + s2
