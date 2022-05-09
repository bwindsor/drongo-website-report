import unittest
from make_report import get_image_caption


class TestAltText(unittest.TestCase):

    def test_one_numeric_prefix(self):
        filename = "0_ben_doing_something_silly.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Ben doing something silly", alt_txt)

    def test_two_numeric_prefixes(self):
        filename = "0_0_john_does_something.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("John does something", alt_txt)

    def test_day_prefix(self):
        filename = "day0_1_ben_john_jeremy_chairlift_selfie.JPG"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Ben john jeremy chairlift selfie", alt_txt)

    def test_other_text_prefix(self):
        filename = "section1_1_natalie_won_the_party.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Natalie won the party", alt_txt)

    def test_non_integer_prefix(self):
        filename = "1_5.5_orienteering_terrain.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Orienteering terrain", alt_txt)

    def test_filename_with_hyphens(self):
        filename = "1-2-ben-eating-an-entire-apple.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Ben eating an entire apple", alt_txt)

    def test_nasty_filename_with_spaces(self):
        filename = "2 jeremy did not finish his food.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Jeremy did not finish his food", alt_txt)

    def test_filename_with_mixed_delimiters(self):
        filename = "1_2-drongo-group photo.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Drongo group photo", alt_txt)

    def test_filename_without_numeric_prefix(self):
        filename = "drongo_group-photo.jpg"
        alt_txt = get_image_caption(filename)
        self.assertEqual("Drongo group photo", alt_txt)
