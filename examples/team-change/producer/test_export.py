import json
import unittest

from checks import cli


class ExportTests(unittest.TestCase):
    def test_currency_and_cents(self):
        order = json.loads(cli("export.py", "--cents", "5"))
        self.assertEqual(order, {"order": "A-17", "total_cents": 5, "currency": "USD"})
