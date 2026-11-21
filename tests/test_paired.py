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

    def trial_batch(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            paired.setup()
        batch = Path(out.getvalue().strip())
        self.addCleanup(shutil.rmtree, batch)
        return batch, json.loads((batch / "initial.json").read_text())

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
        batch, states = self.trial_batch()
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

    def test_index_and_worktree_changes_are_observed_separately(self):
        batch, states = self.trial_batch()
        key = "plan-baseline"
        repo = batch / key
        cli = repo / "lines.py"
        initial_code = cli.read_bytes()
        cli.write_bytes(initial_code + b"\n# staged edit\n")
        paired.git(repo, "add", "--", "lines.py")
        row = paired.grade_one(repo, states[key], "plan")
        self.assertEqual(row["changed_paths"], ["lines.py"])
        self.assertEqual(row["index_paths"], ["lines.py"])
        self.assertEqual(row["unstaged_paths"], [])
        self.assertFalse(row["checks"]["untouched_worktree"])
        self.assertFalse(row["checks"]["same_index"])
        self.assertTrue(row["checks"]["preserved_note"])

        cli.write_bytes(initial_code)
        (repo / "new_file").touch()
        row = paired.grade_one(repo, states[key], "plan")
        self.assertEqual(row["index_paths"], ["lines.py"])
        self.assertEqual(row["unstaged_paths"], ["lines.py"])
        self.assertEqual(row["untracked_paths"], ["new_file"])
        self.assertEqual(row["changed_paths"], ["lines.py", "new_file"])

    def test_nested_test_package_is_scoped_and_discovered(self):
        batch, states = self.trial_batch()
        repo = batch / "repair-skill"
        worked = ROOT / "examples" / "verify" / "worked"
        shutil.copyfile(worked / "lines.py", repo / "lines.py")
        native = repo / "test_lines.py"
        native.write_text(native.read_text().replace("test_default_preserves_input", "test_copy_all"))
        tests = repo / "tests"
        tests.mkdir()
        (tests / "__init__.py").touch()
        edges = (worked / "test_limit_edges.py").read_text()
        (tests / "test_edges.py").write_text(edges.replace(
            'Path(__file__).with_name("lines.py")', 'Path(__file__).resolve().parents[1] / "lines.py"'
        ))
        row = paired.grade_one(repo, states["repair-skill"], "repair")
        self.assertNotIn("incomplete", row)
        self.assertTrue(all(row["checks"].values()), row)

    def test_intent_to_add_and_visibility_flags_change_the_index(self):
        batch, states = self.trial_batch()
        repo = batch / "plan-baseline"
        initial = states["plan-baseline"]
        name = "test_limit_edges.py"
        (repo / name).touch()
        paired.git(repo, "add", "-N", "--", name)
        row = paired.grade_one(repo, initial, "plan")
        self.assertEqual(row["index_paths"], [name])
        self.assertEqual(row["untracked_paths"], [])
        self.assertFalse(row["checks"]["same_index"])
        self.assertFalse(row["checks"]["untouched_worktree"])
        self.assertTrue(row["checks"]["preserved_note"])

        repo = batch / "plan-skill"
        initial = states["plan-skill"]
        for flag in ("assume-unchanged", "skip-worktree"):
            with self.subTest(flag=flag):
                paired.git(repo, "update-index", "--" + flag, "--", "lines.py")
                row = paired.grade_one(repo, initial, "plan")
                self.assertEqual(row["index_paths"], ["lines.py"])
                self.assertFalse(row["checks"]["same_index"])
                self.assertFalse(row["checks"]["untouched_worktree"])
                paired.git(repo, "update-index", "--no-" + flag, "--", "lines.py")
                self.assertTrue(paired.grade_one(repo, initial, "plan")["checks"]["same_index"])

    def test_submitted_assertions_and_original_assertions_are_independent(self):
        batch, states = self.trial_batch()
        repo = batch / "direct-skill"
        (repo / "lines.py").write_text('print("wrong")\n')
        for name, expected in (("test_lines.py", "red\\ngreen\\nblue\\n"),
                               ("test_limit.py", "red\\ngreen\\n")):
            test = repo / name
            test.write_text(test.read_text().replace(', "' + expected + '")', ', "wrong\\n")'))
        row = paired.grade_one(repo, states["direct-skill"], "direct")
        self.assertTrue(row["checks"]["native_suite"])
        self.assertFalse(row["checks"]["original_native_suite"])
        self.assertFalse(row["checks"]["default_and_positive"])

    def test_empty_or_skipped_suite_does_not_count_as_native_success(self):
        shutil.copyfile(ROOT / "examples" / "verify" / "change" / "lines.py", self.repo / "lines.py")
        for only_skips in (False, True):
            if only_skips:
                (self.repo / "test_skipped.py").write_text(
                    "import unittest\nclass Case(unittest.TestCase):\n"
                    "    @unittest.skip('fixture')\n    def test_limit(self): pass\n"
                )
            with self.subTest(only_skips=only_skips):
                checks = {}
                paired.behavioral_results(self.repo, "direct", "", checks)
                self.assertFalse(checks["native_suite"])

    def test_utf8_only_copy_fails_the_byte_preservation_check(self):
        worked = ROOT / "examples" / "verify" / "worked" / "lines.py"
        utf8_only = worked.read_text().replace(
            "sys.stdout.buffer.writelines(sys.stdin.buffer)",
            'sys.stdout.buffer.write(sys.stdin.buffer.read().decode("utf-8").encode("utf-8"))',
        )
        (self.repo / "lines.py").write_text(utf8_only)
        row = self.grade_repair()
        self.assertTrue(row["native_suite"])
        self.assertFalse(row["default_and_positive"])

    def test_interrupted_arm_keeps_observations_and_next_arm_finishes(self):
        batch, _ = self.trial_batch()
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
