import unittest
from make_report import get_image_caption


class TestAltText(unittest.TestCase):

    def test_one_numeric_prefix(self):
        alt_txt = get_image_caption("0_ben_doing_something_silly.jpg")
        self.assertEqual("Ben doing something silly", alt_txt)

    def test_two_numeric_prefixes(self):
        alt_txt = get_image_caption("0_0_john_does_something.jpg")
        self.assertEqual("John does something", alt_txt)

    def test_day_prefix(self):
        alt_txt = get_image_caption("day0_1_ben_john_jeremy_chairlift_selfie.JPG")
        self.assertEqual("Ben john jeremy chairlift selfie", alt_txt)

    def test_non_integer_prefix(self):
        alt_txt = get_image_caption("1_5.5_orienteering_terrain.jpg")
        self.assertEqual("Orienteering terrain", alt_txt)
