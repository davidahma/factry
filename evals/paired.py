"""Set up or score six independent developer skill trials using local Git and Python."""

import argparse
import importlib.util
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = ("plan", "direct", "repair")
ARMS = ("baseline", "skill")
NOTE = "My staged note for a separate change.\n"


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.check_output(["git", *args], cwd=repo, env=env)


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
                (repo / "NOTE.txt").write_text(NOTE)
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


def behavioral_results(repo, case, old_source):
    result = {}
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
    # Reuse the arm's suite against three known implementations in this scratch copy.
    # Selective repairs show whether tests would catch either boundary independently.
    marker = "islice(sys.stdin.buffer, args.limit) if args.limit else"
    if old_source.count(marker) != 1:
        raise ValueError("Review the regression controls for the updated starting fixture")
    replacements = {
        "red_on_original": marker,
        "detects_zero_regression": "islice(sys.stdin.buffer, min(sys.maxsize, args.limit)) if args.limit else",
        "detects_large_regression": "islice(sys.stdin.buffer, args.limit) if args.limit is not None else",
    }
    for label, replacement in replacements.items():
        (repo / "lines.py").write_text(old_source.replace(marker, replacement))
        status, originals_pass, failures = suite(repo)
        result[label] = result["native_suite"] and status == 1 and originals_pass and bool(failures)
    return result


def grade_one(repo, initial, case):
    state = repository_state(repo)
    paths = changed_paths(repo)
    results = {
        "same_refs_head_and_branch": all(state[k] == initial[k] for k in ("refs", "head", "branch")),
        "same_index": state["index"] == initial["index"],
        "preserved_note": (repo / "NOTE.txt").is_file() and
                          (repo / "NOTE.txt").read_bytes() == NOTE.encode(),
    }
    if case == "plan":
        results["untouched_worktree"] = not paths
    else:
        results["expected_patch_paths"] = all(
            p == "lines.py" or (Path(p).name.startswith("test") and p.endswith(".py"))
            for p in paths
        )
        old_source = git(repo, "show", initial["head"] + ":lines.py").decode()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "checkout"
            shutil.copytree(repo, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            results.update(behavioral_results(source, case, old_source))
    return {"changed_paths": paths, "checks": results}


def grade(batch):
    states = json.loads((batch / "initial.json").read_text())
    for case in CASES:
        for arm in ARMS:
            key = f"{case}-{arm}"
            print(json.dumps({"trial": key, **grade_one(batch / key, states[key], case)}))


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
