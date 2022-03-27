import math


def belt_capacity(belt_ca, v):
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


def belt_ca(l3, b, ia, sa):
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
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)

    # Upper half of the belt
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)

    # Lower half of the belt
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s1 + s2
