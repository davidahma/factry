import unittest

from checks import cli


class HelpTests(unittest.TestCase):
    def test_export_help(self):
        self.assertIn(b"Export one order as JSON.", cli("export.py", "--help"))
