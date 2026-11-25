"""Create a disposable repository for the guide handoff walkthrough."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
BASE_FILES = (
    ".github/workflows/ci.yml",
    ".gitignore",
    "AGENTS.md",
    "ISSUE.md",
    "README.md",
    "checks/rollout.py",
    "docs/architecture.md",
    "docs/development.md",
    "docs/testing.md",
    "ledger.py",
    "tests/test_ledger.py",
)
ROLLOUT_OK = "Rollback reader accepted old and current rows: 200\n"
ROLLOUT_FAILURE = "Rollback reader could not read the current row: missing total_pence\n"
BASE_TESTS = ("test_current_round_trip", "test_reads_historical_record")
UPGRADE_TESTS = ("test_writer_adds_amount_minor", "test_reader_totals_old_and_new_rows")


def git(repo, *args):
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        GIT_AUTHOR_DATE="2025-01-01T12:00:00Z",
        GIT_COMMITTER_DATE="2025-01-01T12:00:00Z",
    )
    result = subprocess.run(
        ["git", *args], cwd=repo, env=env, check=True, text=True, stdout=subprocess.PIPE,
    )
    return result.stdout.strip()


def commit(repo, message):
    git(repo, "add", ".")
    git(repo, "commit", "-qm", message)


def build_base(repo):
    git(repo, "init", "-q", "--initial-branch=main", "--template=")
    git(repo, "config", "user.name", "Factry Example")
    git(repo, "config", "user.email", "factry@example.invalid")
    git(repo, "config", "core.autocrlf", "false")
    for name in BASE_FILES:
        destination = repo / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE / "base" / name, destination)
    commit(repo, "Record the requested rename and existing repository rules")


def run_python(repo, *args):
    return subprocess.run(
        [sys.executable, "-B", *args], cwd=repo, capture_output=True, text=True,
    )


def check_unit_suite(repo, passing):
    result = run_python(repo, "-m", "unittest", "discover", "-s", "tests", "-v")
    if result.returncode:
        raise RuntimeError(result.stderr)
    for test in passing:
        if not any(line.startswith(test + " (") and line.endswith(" ... ok")
                   for line in result.stderr.splitlines()):
            raise RuntimeError(f"Expected the ledger suite to pass {test}")


def check_rollout(repo, compatible):
    result = run_python(repo, "checks/rollout.py")
    expected = (0, ROLLOUT_OK, "") if compatible else (1, "", ROLLOUT_FAILURE)
    if (result.returncode, result.stdout, result.stderr) != expected:
        raise RuntimeError(f"Unexpected rollout result: {result}")
    return (result.stdout or result.stderr).strip()


def replay(repo):
    check_unit_suite(repo, BASE_TESTS)
    print("Starting revision: " + git(repo, "rev-parse", "HEAD"))
    print(check_rollout(repo, compatible=True))

    git(repo, "checkout", "-qb", "rollout-ready")
    shutil.copyfile(HERE / "worked" / "ledger.py", repo / "ledger.py")
    shutil.copyfile(HERE / "worked" / "test_amount.py", repo / "tests" / "test_amount.py")
    commit(repo, "Introduce the new field and keep the rollout reader working")
    check_unit_suite(repo, BASE_TESTS + UPGRADE_TESTS)
    print("Worked candidate: " + git(repo, "rev-parse", "HEAD"))
    print(check_rollout(repo, compatible=True))

    git(repo, "checkout", "-qb", "rollout-incompatible")
    ledger = repo / "ledger.py"
    # Keep both readers and the new-field regression, but simulate a premature writer switch.
    original = ledger.read_text(encoding="utf-8")
    broken = original.replace('{"total_pence": amount, "amount_minor": amount}', '{"amount_minor": amount}')
    if original == broken:
        raise RuntimeError("The worked writer no longer emits both fields")
    ledger.write_text(broken, encoding="utf-8")
    commit(repo, "Switch the writer to the new field")
    check_unit_suite(repo, BASE_TESTS + UPGRADE_TESTS)
    print("Incompatible revision: " + git(repo, "rev-parse", "HEAD"))
    print(check_rollout(repo, compatible=False))
    git(repo, "checkout", "-q", "rollout-ready")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="self-test the walkthrough and clean up")
    mode.add_argument("--worked", action="store_true", help="include both worked branches")
    args = parser.parse_args()

    repo = Path(tempfile.mkdtemp(prefix="factry-guide-handoff-"))
    keep = False
    try:
        build_base(repo)
        if args.check or args.worked:
            replay(repo)
        if args.check:
            print("Guide handoff walkthrough self-test passed.")
        else:
            print(repo)
            keep = True
    finally:
        if not keep:
            shutil.rmtree(repo)


if __name__ == "__main__":
    main()
