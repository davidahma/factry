"""Exercise the public ledger commands."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args, data=None):
    return subprocess.check_output(
        [sys.executable, "-B", "ledger.py", *args], input=data, text=True, cwd=ROOT,
    )


class LedgerTest(unittest.TestCase):
    def test_current_round_trip(self):
        receipt = run("write", "125")
        self.assertEqual(len(receipt.splitlines()), 1)
        self.assertIsInstance(json.loads(receipt), dict)
        self.assertEqual(run("total", data=receipt), "125\n")

    def test_reads_historical_record(self):
        self.assertEqual(run("total", data='{"total_pence": 75}\n'), "75\n")
