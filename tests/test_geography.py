import unittest

from core.geography import CITY_COORDINATES, locate


class GeographyTests(unittest.TestCase):
    def test_demo_directory_contains_us_cities(self):
        self.assertGreaterEqual(len(CITY_COORDINATES), 12)
        self.assertEqual(locate("Miami, FL"), (25.7617, -80.1918))
        self.assertIsNone(locate("Unknown"))
