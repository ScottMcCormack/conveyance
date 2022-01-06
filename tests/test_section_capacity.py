import unittest

from conveyance import cross_section


class TestSectionCapacity(unittest.TestCase):
    def setUp(self):
        # Cross-sectional dimensions
        self.l3 = 0.436
        self.b = 1.03
        self.ia = 45
        self.sa = 20

        # Belt speed
        self.v = 4.8

    def test_upper_belt_ca(self):
        s1 = cross_section._upper_belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s1, 0.0445, 4)

    def test_lower_belt_ca(self):
        s1 = cross_section._lower_belt_ca(l3=self.l3, b=self.b, ia=self.ia)
        self.assertAlmostEqual(s1, 0.1357, 4)

    def test_belt_capacity(self):
        s = cross_section.belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s, 0.180, 3)

        q_vt = cross_section.belt_capacity(belt_ca=s, v=self.v)
        self.assertAlmostEqual(q_vt, 0.865, 3)
