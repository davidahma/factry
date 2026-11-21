import unittest

from test_lines import run_lines


class LimitTest(unittest.TestCase):
    def test_limit_two(self):
        self.assertEqual(run_lines("--limit", "2"), "red\ngreen\n")
