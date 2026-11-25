"""Check the new amount field through the ledger CLI."""

import json
import unittest

from test_ledger import run


class AmountTest(unittest.TestCase):
    def test_writer_adds_amount_minor(self):
        receipt = json.loads(run("write", "125"))
        self.assertEqual(receipt["amount_minor"], 125)

    def test_reader_totals_old_and_new_rows(self):
        records = '{"total_pence": 75}\n{"amount_minor": 125}\n'
        self.assertEqual(run("total", data=records), "200\n")
