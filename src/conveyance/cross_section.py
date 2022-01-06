import math


def belt_ca(l3, b, ia, sa):
    """
    Calculate the cross-sectional area of material on the belt.

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
        The cross-sectional area of material on the belt (|m2|`)

    ... |m2| replace:: m\ :sub:`2`\

    """
    s1 = _upper_belt_ca(l3, b, ia, sa)
    s2 = _lower_belt_ca(l3, b, ia)
    return s1 + s2


def _upper_belt_ca(l3, b, ia, sa):
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)
    return s1


def _lower_belt_ca(l3, b, ia):
    ia_r = math.radians(ia)
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s2
