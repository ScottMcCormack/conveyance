import math


def belt_ca(l3, b, ia, sa):
    s1 = upper_belt_ca(l3, b, ia, sa)
    s2 = lower_belt_ca(l3, b, ia)
    return s1 + s2


def upper_belt_ca(l3, b, ia, sa):
    ia_r = math.radians(ia)
    sa_r = math.radians(sa)
    s1 = (1 / 6) * (l3 + (b - l3) * math.cos(ia_r)) ** 2 * math.tan(sa_r)
    return s1


def lower_belt_ca(l3, b, ia):
    ia_r = math.radians(ia)
    s2 = (l3 + ((b - l3) / 2) * math.cos(ia_r)) * (((b - l3) / 2) * math.sin(ia_r))
    return s2
