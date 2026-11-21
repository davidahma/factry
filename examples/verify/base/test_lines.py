import subprocess
import sys
import unittest
from pathlib import Path


def run_lines(*arguments):
    return subprocess.run(
        [sys.executable, str(Path(__file__).with_name("lines.py")), *arguments],
        input="red\ngreen\nblue\n",
        text=True,
        capture_output=True,
        check=True,
    ).stdout


class LinesTest(unittest.TestCase):
    def test_default_preserves_input(self):
        self.assertEqual(run_lines(), "red\ngreen\nblue\n")
