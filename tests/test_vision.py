import unittest

from core.vision import load_primary_face, similarity


class VisionTests(unittest.TestCase):
    def test_missing_images_do_not_produce_a_match(self):
        self.assertEqual(load_primary_face(None), (None, 0))
        self.assertEqual(similarity(None, None), (None, 0, 0))
