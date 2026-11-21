import unittest

from checks import cli


class ReceiptTests(unittest.TestCase):
    def test_receipt_from_export(self):
        exported = cli("export.py", "--cents", "5")
        self.assertEqual(cli("render.py", "--receipt", data=exported), b"A-17 $0.05\n")
