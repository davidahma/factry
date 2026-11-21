"""Controls for the offline paired-trial grader."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("paired", ROOT / "evals" / "paired.py")
paired = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(paired)


class GraderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.repo = self.directory / "trial"
        self.repo.mkdir()
        (self.repo / ".git").mkdir()

    def grade_repair(self):
        example = ROOT / "examples" / "verify"
        old = (example / "change" / "lines.py").read_text()
        shutil.copyfile(example / "base" / "test_lines.py", self.repo / "test_lines.py")
        shutil.copyfile(example / "change" / "test_limit.py", self.repo / "test_limit.py")
        checks = {}
        paired.behavioral_results(self.repo, "repair", old, checks)
        return checks

    def test_independent_boundary_regressions(self):
        worked = ROOT / "examples" / "verify" / "worked"
        for name in ("lines.py", "test_limit_edges.py"):
            shutil.copyfile(worked / name, self.repo / name)
        checks = self.grade_repair()
        self.assertTrue(all(checks.values()), checks)

    def test_private_helper_failures_cannot_earn_mutation_credit(self):
        fixed = (ROOT / "examples" / "verify" / "worked" / "lines.py").read_text()
        (self.repo / "lines.py").write_text(fixed + "\nPRIVATE_MARKER = True\n")
        (self.repo / "test_private.py").write_text(
            "import unittest\n"
            "class PrivateTest(unittest.TestCase):\n"
            "    def test_helper(self):\n"
            "        from lines import PRIVATE_MARKER\n"
            "        self.assertTrue(PRIVATE_MARKER)\n"
        )
        checks = self.grade_repair()
        self.assertTrue(checks["native_suite"])
        self.assertTrue(checks["zero_limit"] and checks["large_limit"])
        self.assertFalse(checks["fully_repaired_control"])
        for key in ("red_on_original", "detects_zero_regression", "detects_large_regression"):
            self.assertFalse(checks[key], key)

    def test_outside_file_link_and_unexpected_files_are_never_opened(self):
        external = self.directory / "outside"
        external.write_text("private fixture sentinel")
        link = self.repo / "NOTE.txt"
        try:
            link.symlink_to(external)
        except OSError as exc:
            self.skipTest(f"Creating a fixture symlink is unavailable: {exc}")
        for path in (link, self.repo / "unexpected.txt"):
            if path != link:
                link.unlink()
                path.write_text("irrelevant")
            with self.subTest(path=path), patch.object(paired.os, "open", wraps=os.open) as opened:
                with self.assertRaises(ValueError):
                    paired.copy_fixture(self.repo, self.directory / ("copy-" + path.name))
                self.assertFalse(opened.called)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO fixture requires POSIX")
    def test_fifo_is_rejected_before_open(self):
        os.mkfifo(self.repo / "test_input.py")
        with patch.object(paired.os, "open", wraps=os.open) as opened:
            with self.assertRaisesRegex(ValueError, "regular"):
                paired.copy_fixture(self.repo, self.directory / "copy")
            self.assertFalse(opened.called)

    def test_unrequested_plan_file_retains_workspace_evidence(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            paired.setup()
        batch = Path(out.getvalue().strip())
        self.addCleanup(shutil.rmtree, batch)
        states = json.loads((batch / "initial.json").read_text())
        for key in ("plan-baseline", "direct-baseline"):
            repo = batch / key
            (repo / "PLAN.md").write_text("Unrequested draft")
            case = key.split("-")[0]
            row = paired.grade_one(repo, states[key], case)
            self.assertEqual(row["changed_paths"], ["PLAN.md"])
            self.assertTrue(row["checks"]["same_index"])
            self.assertTrue(row["checks"]["preserved_note"])
            if case == "plan":
                self.assertNotIn("incomplete", row)
                self.assertFalse(row["checks"]["untouched_worktree"])
            else:
                self.assertIn("Unexpected fixture path", row["incomplete"])
                self.assertFalse(row["checks"]["expected_patch_paths"])

    def test_interrupted_arm_keeps_observations_and_next_arm_finishes(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            paired.setup()
        batch = Path(out.getvalue().strip())
        self.addCleanup(shutil.rmtree, batch)
        attempts = []

        def simulate(repo, case, old_source, checks):
            attempts.append(case)
            checks["native_suite"] = True
            if len(attempts) == 1:
                raise subprocess.TimeoutExpired("observation", 30)

        with patch.object(paired, "behavioral_results", simulate):
            with contextlib.redirect_stdout(io.StringIO()) as reports:
                paired.grade(batch)
        rows = {row["trial"]: row for row in map(json.loads, reports.getvalue().splitlines())}
        self.assertEqual(len(rows), 6)
        first = rows["direct-baseline"]
        self.assertIn("timed out", first["incomplete"])
        self.assertTrue(first["checks"]["native_suite"])
        self.assertTrue(first["checks"]["preserved_note"])
        self.assertNotIn("incomplete", rows["direct-skill"])
        self.assertTrue(rows["direct-skill"]["checks"]["native_suite"])


if __name__ == "__main__":
    unittest.main()
