"""Create a disposable Lines repository or replay its worked repair."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
BASE_TESTS = ("test_default_preserves_input", "test_limit_two")
EDGE_TESTS = ("test_default_preserves_bytes", "test_negative_limit_is_rejected")
REGRESSIONS = ("test_zero_writes_nothing", "test_large_limit_preserves_available_bytes")


def fixture_git(repo, clean_home):
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
        result = subprocess.run(
            ["git", *args], cwd=repo, env=env, check=True,
            stdout=subprocess.PIPE, text=True,
        )
        return result.stdout.strip()

    return git


def copy_files(stage, repo, filenames):
    for filename in filenames:
        shutil.copyfile(HERE / stage / filename, repo / filename)


def build_repository(repo, git):
    git("init", "--quiet", "--initial-branch=main", "--template=")
    git("config", "user.name", "Factry Example")
    git("config", "user.email", "factry@example.invalid")
    copy_files("base", repo, ("README.md", "lines.py", "test_lines.py", ".gitignore"))
    git("add", ".")
    git("commit", "--quiet", "-m", "Add the line-copy CLI and accepted requirements")
    git("checkout", "--quiet", "-b", "add-limit")
    copy_files("change", repo, ("lines.py", "test_limit.py"))
    git("add", ".")
    git("commit", "--quiet", "-m", "Add the line limit option")


def run_suite(repo, passing, failing=()):
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-m", "unittest", "-v"],
        cwd=repo, stderr=subprocess.PIPE, text=True,
    )
    sys.stderr.write(result.stderr)
    expected_code = 1 if failing else 0
    if result.returncode != expected_code:
        raise RuntimeError(f"Suite returned {result.returncode}, expected {expected_code}")
    outcomes = result.stderr.splitlines()
    for methods, status in ((passing, "ok"), (failing, "FAIL")):
        for method in methods:
            if not any(line.startswith(method + " (") and line.endswith(" ... " + status)
                       for line in outcomes):
                raise RuntimeError(f"Native test {method} did not report {status}")
    if failing and f"FAILED (failures={len(failing)})" not in outcomes:
        raise RuntimeError("Unexpected failure in the candidate run")


def check_candidate(repo):
    result = subprocess.run(
        [sys.executable, "-I", "lines.py", "--limit", "0"], cwd=repo,
        input=b"red\ngreen\nblue\n", capture_output=True, check=True,
    )
    if result.stdout != b"red\ngreen\nblue\n" or result.stderr:
        raise RuntimeError("Fixture no longer exhibits the documented zero-limit behavior")
    large = subprocess.run(
        [sys.executable, "-I", "lines.py", "--limit", str(sys.maxsize + 1)],
        cwd=repo, input=b"one\n", capture_output=True,
    )
    if large.returncode == 0 or b"ValueError" not in large.stderr:
        raise RuntimeError("Fixture no longer exhibits the documented large-limit failure")


def show_repair(repo, git):
    check_candidate(repo)
    print("Confirmed both boundary failures on " + git("rev-parse", "HEAD"), flush=True)
    git("checkout", "--quiet", "-b", "repair-limit")
    copy_files("worked", repo, ("PLAN.md", "test_limit_edges.py"))
    print("Applying PLAN.md. Running its new tests on the original implementation.", flush=True)
    run_suite(repo, BASE_TESTS + EDGE_TESTS, failing=REGRESSIONS)
    copy_files("worked", repo, ("lines.py",))
    git("add", "--", "PLAN.md", "test_limit_edges.py", "lines.py")
    git("commit", "--quiet", "-m", "Honor zero and large line limits")
    repaired = git("rev-parse", "HEAD")
    print("Verifying repaired commit " + repaired, flush=True)
    run_suite(repo, BASE_TESTS + EDGE_TESTS + REGRESSIONS)
    if git("status", "--porcelain") or git("rev-parse", "HEAD") != repaired:
        raise RuntimeError("The verified checkout changed during the run")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="check the exercise and repair, then clean up")
    mode.add_argument("--worked", action="store_true", help="create and verify the worked repair")
    args = parser.parse_args()
    repo = Path(tempfile.mkdtemp(prefix="factry-lines-"))
    keep = False
    try:
        with tempfile.TemporaryDirectory(prefix="factry-git-home-") as clean_home:
            git = fixture_git(repo, clean_home)
            build_repository(repo, git)
            run_suite(repo, BASE_TESTS)
            if args.check or args.worked:
                show_repair(repo, git)
        if args.check:
            print("Walkthrough self-test passed.")
        else:
            comparison = "repair-limit with add-limit" if args.worked else "add-limit with main"
            print(f"Open the following repository in your coding agent. Compare {comparison}.")
            print(repo)
            keep = True
    finally:
        if not keep:
            shutil.rmtree(repo)


if __name__ == "__main__":
    main()
