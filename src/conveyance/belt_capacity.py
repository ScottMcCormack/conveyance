import math


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


def volume_carried_material(q, p):
    """
    Calculate the volume carried per second (m^3/s)

    Parameters
    ----------
    q: float
        Throughput of the conveyor (t/h)
    p: float
        Density of the material (t/m^3)

    Returns
    -------
    float:
        Volume per second of material carried (m^3/s)

    """
    q_v = (1000 * q) / (3600 * p * 1000)
    return q_v


def volumetric_flow(belt_ca, v):
    """
    Calculate the theoretical flow rate of the conveyor

    Parameters
    ----------
    belt_ca: float
        Cross-sectional area of material of the belt (m^2)
    v: float
        Speed of the conveyor belt (m/s)

    Returns
    -------
    float:
        The theoretical flow rate of the conveyor (m^3/s)

    """
    return belt_ca * v


def belt_cs_area(l3, b, ia, sa):
    """
    Calculate the cross-sectional area of material of the belt.

    A three-roll idler set is assumed.

    Parameters
    ----------
    l3: float
        Width of the idler (m)
    b: float
        Width of max material on belt (m)
    ia: float
        Installed angle of the side idlers (deg)
    sa: float
        Surcharge angle of the material (deg)

    Returns
    -------
    float
        The cross-sectional area of material on the belt (m^2)

    """
    # Convert deg inputs to radians
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)

    # Upper half of the belt
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)

    # Lower half of the belt
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s1 + s2
