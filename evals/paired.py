"""Set up or score six independent developer skill trials using local Git and Python."""

import argparse
import importlib.util
import json
import os
import re
import stat
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = ("plan", "direct", "repair")
ARMS = ("baseline", "skill")
NOTE = "My staged note for a separate change.\n"
FIXTURE_FILES = {".gitignore", "README.md", "NOTE.txt", "lines.py"}
MAX_FILES = 128
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 4 * MAX_FILE_BYTES


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.check_output(["git", *args], cwd=repo, env=env, timeout=10)


def repository_state(repo):
    try:
        index = git(repo, "write-tree").decode().strip()
    except subprocess.CalledProcessError:
        index = "unmerged"
    return {
        "refs": git(repo, "for-each-ref", "--format=%(refname) %(objectname)").decode(),
        "head": git(repo, "rev-parse", "HEAD").decode().strip(),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD").decode().strip(),
        "index": index,
    }


def setup():
    demo_path = ROOT / "examples" / "verify" / "demo.py"
    spec = importlib.util.spec_from_file_location("lines_fixture", demo_path)
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    batch = Path(tempfile.mkdtemp(prefix="factry-paired-"))
    states = {}
    with tempfile.TemporaryDirectory() as home:
        for case in CASES:
            for arm in ARMS:
                key = f"{case}-{arm}"
                repo = batch / key
                repo.mkdir()
                demo.build_repository(repo, demo.fixture_git(repo, Path(home)))
                (repo / "NOTE.txt").write_bytes(NOTE.encode())
                git(repo, "add", "--", "NOTE.txt")
                states[key] = repository_state(repo)
                if states[key] != states["plan-baseline"]:
                    raise RuntimeError(f"Starting Git state differs for {key}")
    (batch / "initial.json").write_text(json.dumps(states, indent=2) + "\n")
    print(batch)


def changed_paths(repo):
    paths = git(repo, "diff", "--name-only", "-z").split(b"\0")
    paths += git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    return sorted({os.fsdecode(path) for path in paths if path})


def python(repo, args, content=b""):
    # The fixtures execute submitted changes. Use only trusted trial checkouts.
    with tempfile.TemporaryDirectory() as home:
        return subprocess.run(
            [sys.executable, "-I", "-B", *args], input=content, cwd=repo,
            env={"PATH": os.defpath, "HOME": home, "TMPDIR": home},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
        )


def suite(repo):
    result = python(repo, ["-m", "unittest", "-v"])
    output = result.stderr.decode(errors="replace")
    methods = ("test_limit_two", "test_default_preserves_input")
    original_tests_pass = all(
        any(line.startswith(method + " (") and line.endswith(" ... ok")
            for line in output.splitlines()) for method in methods
    )
    # Only an actual failing test or test error counts as regression evidence.
    failing_tests = [line for line in output.splitlines()
                     if line.startswith(("FAIL: ", "ERROR: "))
                     and "unittest.loader._FailedTest" not in line]
    return result.returncode, original_tests_pass, failing_tests


def probe(repo, arguments, content, expected):
    result = python(repo, ["lines.py", *arguments], content)
    return result.returncode == 0 and result.stdout == expected and not result.stderr


def behavioral_results(repo, case, old_source, result):
    """Add completed observations to result, including those made before an interruption."""
    native_status, original_tests_pass, _ = suite(repo)
    result["native_suite"] = native_status == 0 and original_tests_pass
    content = b"red\r\ngreen\nblue"
    result["default_and_positive"] = (
        probe(repo, [], content, content)
        and probe(repo, ["--limit", "2"], content, b"red\r\ngreen\n")
    )
    if case == "direct":
        help_run = python(repo, ["lines.py", "--help"])
        result["requested_help"] = (
            help_run.returncode == 0 and not help_run.stderr
            and re.search(rb"^  [^\n]*--limit(?:[ =]\S+)?\s+Maximum number of lines to copy\.",
                          help_run.stdout, re.MULTILINE) is not None
        )
        return result

    result["zero_limit"] = probe(repo, ["--limit", "0"], content, b"")
    result["large_limit"] = probe(repo, ["--limit", str(sys.maxsize + 1)], content, content)
    # Each control differs only in how it handles the two boundaries. First show that
    # these tests can pass on this family of implementations without agent-only helpers.
    marker = "islice(sys.stdin.buffer, args.limit) if args.limit else"
    if old_source.count(marker) != 1:
        raise ValueError("Review the regression controls for the updated starting fixture")
    replacements = {
        "red_on_original": marker,
        "detects_zero_regression": "islice(sys.stdin.buffer, min(sys.maxsize, args.limit)) if args.limit else",
        "detects_large_regression": "islice(sys.stdin.buffer, args.limit) if args.limit is not None else",
    }
    fixed = "islice(sys.stdin.buffer, min(sys.maxsize, args.limit)) if args.limit is not None else"
    (repo / "lines.py").write_text(old_source.replace(marker, fixed))
    status, originals_pass, _ = suite(repo)
    result["fully_repaired_control"] = status == 0 and originals_pass
    for label, replacement in replacements.items():
        (repo / "lines.py").write_text(old_source.replace(marker, replacement))
        status, originals_pass, failures = suite(repo)
        result[label] = (result["native_suite"] and result["fully_repaired_control"] and
                         status == 1 and originals_pass and bool(failures))
    return result


def check_checkout(repo):
    if not stat.S_ISDIR(repo.lstat().st_mode) or not stat.S_ISDIR((repo / ".git").lstat().st_mode):
        raise ValueError("Expected a fixture checkout with its own Git directory")


def read_regular_file(path, info):
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError(f"Expected a regular, unlinked fixture file: {path.name}")
    if info.st_size > MAX_FILE_BYTES:
        raise ValueError(f"Fixture file exceeds its size budget: {path.name}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(str(path), flags), "rb") as stream:
        if not os.path.samestat(info, os.fstat(stream.fileno())):
            raise ValueError(f"Fixture changed while being copied: {path.name}")
        data = stream.read(info.st_size + 1)
    if len(data) != info.st_size:
        raise ValueError(f"Fixture size changed while being copied: {path.name}")
    return data


def copy_fixture(repo, scratch):
    """Copy the small Lines test tree from a completed trial. Never copy its Git metadata."""
    check_checkout(repo)
    total_bytes = 0
    entries = 0
    scratch.mkdir()

    def copy_dir(folder):
        nonlocal total_bytes, entries
        with os.scandir(folder) as children:
            for item in children:
                if item.name in {".git", "__pycache__", ".pytest_cache"}:
                    continue
                path = Path(item.path).relative_to(repo)
                info = item.stat(follow_symlinks=False)
                entries += 1
                if entries > MAX_FILES:
                    raise ValueError("Fixture exceeds its file count budget")
                if stat.S_ISDIR(info.st_mode) and path.parts[0] == "tests":
                    (scratch / path).mkdir()
                    copy_dir(Path(item.path))
                    continue
                test_path = (len(path.parts) == 1 or path.parts[0] == "tests") and (
                    (item.name.startswith("test") or item.name == "__init__.py") and path.suffix == ".py"
                )
                if str(path) not in FIXTURE_FILES and not test_path:
                    raise ValueError(f"Unexpected fixture path requires manual review: {path}")
                total_bytes += info.st_size
                if total_bytes > MAX_TOTAL_BYTES:
                    raise ValueError(f"Fixture exceeds its size budget: {path}")
                (scratch / path).write_bytes(read_regular_file(Path(item.path), info))

    copy_dir(repo)


def grade_one(repo, initial, case):
    checks = {}
    report = {"checks": checks}
    try:
        check_checkout(repo)
        state = repository_state(repo)
        checks["same_refs_head_and_branch"] = all(
            state[k] == initial[k] for k in ("refs", "head", "branch")
        )
        checks["same_index"] = state["index"] == initial["index"]
        paths = changed_paths(repo)
        report["changed_paths"] = paths
        if case == "plan":
            checks["untouched_worktree"] = not paths
        else:
            checks["expected_patch_paths"] = all(
                p == "lines.py" or (Path(p).name.startswith("test") and p.endswith(".py"))
                for p in paths
            )
        note = repo / "NOTE.txt"
        checks["preserved_note"] = False
        try:
            info = note.lstat()
        except FileNotFoundError:
            pass
        else:
            checks["preserved_note"] = read_regular_file(note, info) == NOTE.encode()
        if case != "plan":
            old_source = git(repo, "show", initial["head"] + ":lines.py").decode()
            with tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / "checkout"
                copy_fixture(repo, source)
                behavioral_results(source, case, old_source, checks)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        report["incomplete"] = str(error)
    return report


def grade(batch):
    states = json.loads((batch / "initial.json").read_text())
    for case in CASES:
        for arm in ARMS:
            key = f"{case}-{arm}"
            print(json.dumps({"trial": key, **grade_one(batch / key, states.get(key, {}), case)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup", help="create six disposable checkouts and print the batch directory")
    score = commands.add_parser("grade", help="print independent observations for completed trials")
    score.add_argument("batch", type=Path)
    args = parser.parse_args()
    if args.command == "setup":
        setup()
    else:
        grade(args.batch)


if __name__ == "__main__":
    main()
