"""Create the Lines pull request locally, or check the fixture and remove it."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent


def build_repository(repo, clean_home):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(
        HOME=str(clean_home),
        XDG_CONFIG_HOME=str(clean_home),
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_DATE="2025-01-01T12:00:00Z",
        GIT_COMMITTER_DATE="2025-01-01T12:00:00Z",
    )

    def git(*args):
        subprocess.run(["git", *args], cwd=repo, env=env, check=True)

    git("init", "--quiet", "--initial-branch=main", "--template=")
    git("config", "user.name", "Factry Example")
    git("config", "user.email", "factry@example.invalid")
    for filename in ("README.md", "lines.py", "test_lines.py", ".gitignore"):
        shutil.copyfile(HERE / "base" / filename, repo / filename)
    git("add", ".")
    git("commit", "--quiet", "-m", "Add the line-copy CLI and accepted requirements")
    git("checkout", "--quiet", "-b", "add-limit")
    for filename in ("lines.py", "test_limit.py"):
        shutil.copyfile(HERE / "change" / filename, repo / filename)
    git("add", ".")
    git("commit", "--quiet", "-m", "Add the line limit option")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the walkthrough self-test")
    args = parser.parse_args()
    repo = Path(tempfile.mkdtemp(prefix="factry-lines-"))
    keep = False
    try:
        with tempfile.TemporaryDirectory(prefix="factry-git-home-") as clean_home:
            build_repository(repo, clean_home)
        suite = subprocess.run(
            [sys.executable, "-I", "-B", "-m", "unittest", "-v"],
            cwd=repo, stderr=subprocess.PIPE, text=True,
        )
        sys.stderr.write(suite.stderr)
        suite.check_returncode()
        for method in ("test_default_preserves_input", "test_limit_two"):
            passed = any(line.startswith(method + " (") and line.endswith(" ... ok")
                         for line in suite.stderr.splitlines())
            if not passed:
                raise RuntimeError(f"Native suite did not run and pass {method}")
        if args.check:
            result = subprocess.run(
                [sys.executable, "-I", "lines.py", "--limit", "0"],
                cwd=repo,
                input=b"red\ngreen\nblue\n",
                capture_output=True,
                check=True,
            )
            if result.stdout != b"red\ngreen\nblue\n" or result.stderr:
                raise RuntimeError("Fixture no longer exhibits the documented zero-limit behavior")
            large = subprocess.run(
                [sys.executable, "-I", "lines.py", "--limit", str(sys.maxsize + 1)],
                cwd=repo,
                input=b"one\n",
                capture_output=True,
            )
            if large.returncode == 0 or b"ValueError" not in large.stderr:
                raise RuntimeError("Fixture no longer exhibits the documented large-limit failure")
            print("Walkthrough self-test passed.")
        else:
            print("Open the following repository in your coding agent. Compare add-limit with main.")
            print(repo)
            keep = True
    finally:
        if not keep:
            shutil.rmtree(repo)


if __name__ == "__main__":
    main()
