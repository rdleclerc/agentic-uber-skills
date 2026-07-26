import unittest

from formatter import format_name


class FormatterTest(unittest.TestCase):
    def test_trims_surrounding_whitespace(self):
        self.assertEqual("Ada", format_name(" Ada "))
