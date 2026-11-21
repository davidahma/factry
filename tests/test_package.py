"""Exercise the packaged candidate and reject changed release artifacts."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "package.py"


def fixture_git(*args, cwd=ROOT, input_data=None):
    # Test setup and independent readback must address the named fixture, even in a hook.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.check_output(["git", *args], cwd=cwd, env=env, input=input_data)


class ReleaseArchiveTest(unittest.TestCase):
    def test_catalog_is_read_from_the_packaged_revision(self):
        legacy = (
            "address-review", "debug", "fix-ci", "implement", "plan", "post-merge",
            "release", "review", "scout", "ship", "verify",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            fixture_git("init", "-q", "--template=", str(source))
            scripts = source / "scripts"
            scripts.mkdir()
            script = scripts / "package.py"
            script.write_bytes(SCRIPT.read_bytes())
            (source / "LICENSE").write_text("Example license\n")
            for name in legacy:
                folder = source / "skills" / ("factry-" + name)
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(name)

            def commit():
                fixture_git("add", ".", cwd=source)
                fixture_git("-c", "user.name=Fixture", "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "Fixture revision", cwd=source)
                return fixture_git("rev-parse", "HEAD", cwd=source).decode().strip()

            def build(ref, name):
                return subprocess.run([sys.executable, str(script), "build", ref, str(root / name)],
                                      capture_output=True, text=True)

            old = commit()
            result = build(old, "old.zip")
            self.assertEqual(result.returncode, 0, result.stderr)
            catalog = scripts / "skill-catalog.txt"
            names = sorted("factry-" + name for name in (*legacy, "audit"))
            catalog.write_text("\n".join(names) + "\n")
            missing = build(commit(), "missing.zip")
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("skills/factry-audit/SKILL.md", missing.stderr)

            audit = source / "skills" / "factry-audit"
            audit.mkdir()
            (audit / "SKILL.md").write_text("Audit")
            result = build(commit(), "new.zip")
            self.assertEqual(result.returncode, 0, result.stderr)
            with ZipFile(root / "new.zip") as archive:
                self.assertIn("skills/factry-audit/SKILL.md", archive.namelist())
            result = build(old, "old-again.zip")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((root / "old.zip").read_bytes(), (root / "old-again.zip").read_bytes())

            catalog.write_text("\n".join(names + names[:1]))
            invalid = build(commit(), "invalid.zip")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("sorted, unique", invalid.stderr)

    def test_git_environment_and_replacement_objects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            caller = root / "caller"
            fixture_git("init", "-q", "--template=", str(caller))
            inherited = {"GIT_DIR": str(caller / ".git"), "GIT_WORK_TREE": str(caller)}
            with patch.dict(os.environ, inherited):
                fixture_git("clone", "-q", "--no-local", str(ROOT), str(source))
            script = source / "scripts" / "package.py"
            script.write_bytes(SCRIPT.read_bytes())

            def build(target, env=None):
                subprocess.run([sys.executable, str(script), "build", "HEAD", str(target)],
                               env=env, check=True, capture_output=True)

            expected = root / "expected.zip"
            build(expected)
            isolated = root / "isolated.zip"
            with patch.dict(os.environ, inherited):
                blob = fixture_git("rev-parse", "HEAD:LICENSE", cwd=source).strip()
                new = fixture_git("hash-object", "-w", "--stdin", cwd=source,
                                  input_data=b"replaced license").strip()
                fixture_git("replace", blob, new, cwd=source)
                self.assertEqual(fixture_git("show", "HEAD:LICENSE", cwd=source), b"replaced license")
                build(isolated)
            self.assertEqual(fixture_git("for-each-ref", cwd=caller), b"")
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
            commit = fixture_git("rev-parse", "HEAD").strip()
            tree = fixture_git("--no-replace-objects", "ls-tree", "-r", "-z",
                               "HEAD", "--", "LICENSE", "skills")
            with ZipFile(archive) as packed:
                self.assertEqual(packed.comment, commit)
                self.assertEqual(len(packed.namelist()), len(tree.rstrip(b"\0").split(b"\0")))
                for record in tree.rstrip(b"\0").split(b"\0"):
                    metadata, name = record.split(b"\t", 1)
                    blob_sha = metadata.split()[2]
                    original = fixture_git("--no-replace-objects", "cat-file", "blob", blob_sha)
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
