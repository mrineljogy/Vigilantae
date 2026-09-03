"""Tests for the shared U.S. map coordinate directory."""

import unittest

from pages.helper.locations import US_CENTER, city_coordinates


class LocationTests(unittest.TestCase):
    def test_resolves_city_case_insensitively(self):
        self.assertEqual(city_coordinates("chicago"), (41.8781, -87.6298))

    def test_resolves_common_aliases(self):
        self.assertEqual(city_coordinates("NYC"), city_coordinates("New York"))
        self.assertEqual(city_coordinates("DC"), city_coordinates("Washington, DC"))
        self.assertEqual(city_coordinates("Miami, USA"), city_coordinates("Miami"))

    def test_resolves_states_for_forgiving_demo_input(self):
        self.assertEqual(city_coordinates("Ohio USA"), (40.3888, -82.7649))

    def test_unknown_city_has_no_marker_location(self):
        self.assertIsNone(city_coordinates("Not A Real U.S. City"))
        self.assertEqual(city_coordinates(None), US_CENTER)


if __name__ == "__main__":
    unittest.main()
