import unittest

from conveyance import cross_section


class TestSectionCapacity(unittest.TestCase):
    def setUp(self):
        self.l3 = 0.436
        self.b = 1.03
        self.ia = 45
        self.sa = 20

    def test_upper_belt_ca(self):
        s1 = cross_section.upper_belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s1, 0.0445, 4)

    def test_lower_belt_ca(self):
        s1 = cross_section.lower_belt_ca(l3=self.l3, b=self.b, ia=self.ia)
        self.assertAlmostEqual(s1, 0.1357, 4)

    def test_belt_ca(self):
        s = cross_section.belt_ca(l3=self.l3, b=self.b, ia=self.ia, sa=self.sa)
        self.assertAlmostEqual(s, 0.180, 3)

