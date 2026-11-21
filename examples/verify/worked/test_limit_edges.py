import subprocess
import sys
import unittest
from pathlib import Path


def invoke(*arguments):
    return subprocess.run(
        [sys.executable, str(Path(__file__).with_name("lines.py")), *arguments],
        input=b"red\r\n\xff\nblue",
        capture_output=True,
    )


class LimitEdgesTest(unittest.TestCase):
    def test_zero_writes_nothing(self):
        result = invoke("--limit", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"")

    def test_large_limit_preserves_available_bytes(self):
        result = invoke("--limit", str(sys.maxsize + 1))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"red\r\n\xff\nblue")

    def test_default_preserves_bytes(self):
        result = invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, b"red\r\n\xff\nblue")

    def test_negative_limit_is_rejected(self):
        result = invoke("--limit", "-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--limit must be nonnegative", result.stderr)
        self.assertEqual(result.stdout, b"")
