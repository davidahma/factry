"""Exercise the packaged candidate and reject changed release artifacts."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package.py"


class ReleaseArchiveTest(unittest.TestCase):
    def test_git_environment_and_replacement_objects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            subprocess.run(["git", "clone", "-q", "--no-local", str(ROOT), str(source)], check=True)
            script = source / "scripts" / "package.py"
            script.write_bytes(SCRIPT.read_bytes())

            def build(target, env=None):
                subprocess.run([sys.executable, str(script), "build", "HEAD", str(target)],
                               env=env, check=True, capture_output=True)

            expected = root / "expected.zip"
            build(expected)
            blob = subprocess.check_output(["git", "rev-parse", "HEAD:LICENSE"], cwd=source).strip()
            new = subprocess.check_output(["git", "hash-object", "-w", "--stdin"],
                                          cwd=source, input=b"replaced license").strip()
            subprocess.run(["git", "replace", blob, new], cwd=source, check=True)
            isolated = root / "isolated.zip"
            build(isolated, dict(os.environ, GIT_DIR=str(root / "another.git"),
                                 GIT_WORK_TREE=str(root / "another")))
            self.assertEqual(expected.read_bytes(), isolated.read_bytes())

    def test_candidate_and_corrupt_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "factry.zip"

            def run(action, dest):
                return subprocess.run(
                    [sys.executable, str(SCRIPT), action, "HEAD", str(dest)],
                    capture_output=True, text=True,
                )

            built = run("build", archive)
            self.assertEqual(built.returncode, 0, built.stderr)
            verified = run("verify", archive)
            self.assertEqual(verified.returncode, 0, verified.stderr)

            # Unpack the legitimate result independently and compare it with Git.
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).strip()
            tree = subprocess.check_output(
                ["git", "ls-tree", "-r", "-z", "HEAD", "--", "LICENSE", "skills"], cwd=ROOT
            )
            with ZipFile(archive) as packed:
                self.assertEqual(packed.comment, commit)
                self.assertEqual(len(packed.namelist()), len(tree.rstrip(b"\0").split(b"\0")))
                for record in tree.rstrip(b"\0").split(b"\0"):
                    metadata, name = record.split(b"\t", 1)
                    blob_sha = metadata.split()[2]
                    original = subprocess.check_output(["git", "cat-file", "blob", blob_sha], cwd=ROOT)
                    self.assertEqual(packed.read(name.decode("utf-8")), original)

            for mutation in ("wrong bytes", "missing skill", "trailing bytes"):
                with self.subTest(mutation=mutation):
                    invalid = Path(directory) / "invalid.zip"
                    if mutation == "trailing bytes":
                        invalid.write_bytes(archive.read_bytes() + b"extra")
                    else:
                        with ZipFile(archive) as original, ZipFile(invalid, "w") as changed:
                            changed.comment = original.comment
                            for entry in original.infolist():
                                if entry.filename == "skills/factry-plan/SKILL.md":
                                    if mutation == "missing skill":
                                        continue
                                    changed.writestr(entry, b"unreviewed text")
                                else:
                                    changed.writestr(entry, original.read(entry))
                    refused = run("verify", invalid)
                    self.assertNotEqual(refused.returncode, 0)
                    self.assertIn("Archive differs", refused.stderr)


if __name__ == "__main__":
    unittest.main()
