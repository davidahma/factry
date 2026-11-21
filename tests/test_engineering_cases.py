"""Keep the four published engineering trial inputs reproducible in a fresh checkout."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SETUP = Path(__file__).resolve().parents[1] / "evals" / "engineering" / "setup.py"


class EngineeringCasesTest(unittest.TestCase):
    def test_documented_controls_and_failure_cases(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory) / "checkouts"
            subprocess.run([sys.executable, str(SETUP), str(batch)], check=True, capture_output=True)

            def run(project, *args):
                return subprocess.run([sys.executable, "-B", *args], cwd=batch / project,
                                      text=True, capture_output=True)

            for name in ("channel", "ledger", "outbox"):
                with self.subTest(project=name):
                    native = run(name, "-m", "unittest", "-v")
                    self.assertEqual(native.returncode, 0, native.stderr)
                    self.assertIn("Ran 1 test", native.stderr)

            ordinary = run("channel", "channel.py", "32767")
            self.assertEqual((ordinary.returncode, ordinary.stdout), (0, "7fff\n"))
            self.assertNotEqual(run("channel", "channel.py", "32768").returncode, 0)

            old_reader = run("ledger", "-c", """from billing import total
print(total(['{"amount_minor": 5}']))
""")
            self.assertNotEqual(old_reader.returncode, 0)
            self.assertIn("KeyError", old_reader.stderr)

            duplicate = run("outbox", "-c", """from outbox import deliver
class Queue(list):
    def append(self, record):
        super().append(record)
        if len(self) == 1:
            raise TimeoutError()
record = {"id": "17", "text": "ready"}
sent, queue = set(), Queue()
try:
    deliver(record, sent, queue)
except TimeoutError:
    pass
deliver(record, sent, queue)
print([r["id"] for r in queue])
""")
            self.assertEqual((duplicate.returncode, duplicate.stdout), (0, "['17', '17']\n"))
            self.assertIn("milepost.py stats", (batch / "milepost/README.md").read_text())
            self.assertNotEqual(run("milepost", "milepost.py", "stats").returncode, 0)
            count = run("milepost", "milepost.py", "count")
            self.assertEqual((count.returncode, count.stdout), (0, "3\n"))
