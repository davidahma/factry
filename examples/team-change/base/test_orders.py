import unittest

from checks import cli


class ContractTests(unittest.TestCase):
    def test_default_round_trip(self):
        self.assertEqual(cli("render.py", data=cli("export.py")), b"A-17 1250\n")
