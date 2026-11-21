import unittest

from checks import cli


class ExtensionTests(unittest.TestCase):
    def test_renderer_accepts_additional_fields(self):
        data = b'{"order":"B-2","total_cents":203,"warehouse":"east"}'
        self.assertEqual(cli("render.py", data=data), b"B-2 203\n")
        self.assertEqual(cli("render.py", "--receipt", data=data), b"B-2 $2.03\n")
